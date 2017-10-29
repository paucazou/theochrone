#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the Matcher class"""
import Levenshtein
import os
import phlog
import pickle
import re
import splitter

logger = phlog.loggers['console']

class Matcher:
    """Implements the functions for a good research
    for specified tokens"""
    
    _word_frequency_dic = {} # {lang:tuple(words,wordcost,maxword)}
    regex = re.compile(r"(?ui)\W") # https://github.com/seatgeek/fuzzywuzzy/blob/master/fuzzywuzzy/string_processing.py
    
    def __init__(self,tokens,lang):
        """tokens are a list of strings
        lang = a language code (fr,en,es...)"""
        self.lang = lang
        self._set_tokens(tokens) # set self.tokens
        self.reset_scores() # save the best fuzz score 

    def fuzzer(self,text,with_distance_ratio=True):
        """Return the ratio for self.tokens
        againt text.
        text : str
        return an int as ratio, between 0 to 100
        with_distance_ratio = if the distance between
        tokens matching in the text must be taken in account"""
        token_pos = { token: {'index':0,'score':0} for token in self.tokens }
        
        #text = re.sub("""[\.,;?:!"-']""",' ',text)
        text = self.regex.sub(" ",text)
        text = [word for word in text.lower().split() if len(word) > 2 ]
        ratio = 0
        for token in self.tokens:
            token_ratio = 0
            for index, word in enumerate(text):
                word_ratio = Levenshtein.ratio(token,word)
                if word_ratio > token_ratio:
                    token_ratio = word_ratio
                    token_pos[token]['index'] = index
                    token_pos[token]['score'] = token_ratio
                    if word_ratio > self._best_score[token]:
                        self._best_score[token] = word_ratio
                if word_ratio == 1:
                    break
            ratio += token_ratio
        final_ratio = ratio / self.token_nb
        
        if with_distance_ratio: # taking distance in count
            distance_ratio = self.word_distance(token_pos)
            if final_ratio > 0.85 and distance_ratio >= 0.0001:
                logger.debug('{} : {}'.format(self.tokens,text))
            final_ratio -= distance_ratio
            
        return final_ratio

    def word_distance(self,token_pos): # can't really discover approximate words -> try with fuzz ?
        """Takes token_pos dict, the number of tokens (self.token_nb)
        and return the distance ratio :
        if ratio is equal to token_nb = 0
        The distance ratio is very low, for it is just intended to discriminate
        equal high results"""
        if self.token_nb == 1: # case of an only token
            return 0
        
        values = tuple(value['index'] for value in sorted(token_pos.values(),key=lambda x:x['index']) if value['score'] > 0.85)
        if not values:
            return 0
        
        raw_distance = max(values) - min(values) + 1 # problème à prévoir avec l'index 0 ?
        #logger.debug("raw_distance : {}".format(raw_distance))
        
        # managing the case of a token which has a score lower than 0.85
        len_diff = self.token_nb - len(values)
        #logger.debug("len_diff : {}".format(len_diff))
        len_diff = (-len_diff,len_diff)[raw_distance > self.token_nb]
        #logger.debug('new len_diff : {}'.format(len_diff))
        
        mod_distance = raw_distance + len_diff
        distance_ratio = abs((mod_distance/self.token_nb -1) * 0.00001)
        
        return distance_ratio
    
    def is_score_low(self,floor=0.85):
        """Checks the height of self._best_score
        and return True if one of the score is under
        floor."""
        return True if min(self._best_score.values()) < floor else False
    
    def reset_scores(self):
        """Reset best score to 0"""
        self._best_score = {token:0 for token in self.tokens }
        
    def splitter(self,floor=0.85):
        """In this method, tokens with best score under floor
        are considered to lack some spaces.
        This method modifies them with the help of self._word_frequency_dic, which is
        a tuple(words,{word:wordcost},maxword}
        If they are really modified, return True
        If not, return False"""
        temp_tokens = { token for token in self.tokens if self._best_score[token] < floor}
        self.tokens.difference_update(temp_tokens)
        logger.debug(temp_tokens)
        ntokens = set()
        for token in temp_tokens:
            token = splitter.infer_spaces(token,*self._call_word_frequency_dic())
            logger.debug(token)
            ntokens.add(token)
        if not temp_tokens or ntokens == temp_tokens:
            are_tokens_modified = False
        else:
            self._set_tokens(ntokens,True)
            are_tokens_modified = True
            logger.debug(self.tokens)
        return are_tokens_modified
    
    def _call_word_frequency_dic(self):
        """Loads the dictionary of words frequency
        and update cls._word_frequency_dic for self.lang"""
        if self.lang not in self._word_frequency_dic:
            path = os.path.dirname(splitter.__file__) + '/'
            with open(path + '/data/' + self.lang + '_word_frequency.pkl','rb') as file:
                self._word_frequency_dic[self.lang] = pickle.Unpickler(file).load()
        return self._word_frequency_dic[self.lang]
            
    def _set_tokens(self,tokens,update=False):
        """Create self.tokens or update them
        Set self.token_nb also"""
        tokens = " ".join(tokens)
        #tokens = re.sub("""[\.,;?:!-']""",' ',tokens)
        tokens = self.regex.sub(" ",tokens)
        tokens = {token.lower() for token in tokens.split() if len(token) > 2}
        if update:
            self.tokens.update(tokens)
        else:
            self.tokens = tokens
        self.token_nb = len(self.tokens)
        

