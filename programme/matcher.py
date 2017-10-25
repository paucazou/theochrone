#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the Matcher class"""
import Levenshtein
import phlog
import re

logger = phlog.loggers['console']

class Matcher:
    """Implements the functions for a good research
    for specified tokens"""
    
    def __init__(self,tokens):
        """tokens are a list of strings"""
        tokens = " ".join(tokens)
        tokens = re.sub("""[\.,;?:!"]""","",tokens) 
        tokens = re.sub("""[-']""",' ',tokens)
        self.tokens = {token.lower() for token in tokens.split() if len(token) > 2}
        self.token_nb = len(self.tokens)
        self._best_score = {token:0 for token in self.tokens } # save the best fuzz score 

    def fuzzer(self,text,with_distance_ratio=True):
        """Return the ratio for self.tokens
        againt text.
        text : str
        return an int as ratio, between 0 to 100
        with_distance_ratio = if the distance between
        tokens matching in the text must be taken in account"""
        token_pos = { token: {'index':0,'score':0} for token in self.tokens }
        
        text = re.sub("""[\.,;?:!"]""","",text) 
        text = re.sub("""[-']""",' ',text)
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

    def word_distance(self,token_pos):
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
    
    



"""
au cas où un mot n'ait pas atteint le score de 0.5 une seule fois :
on fait appel à word_frequency (changer ce nom inadapté), et, en cas de nouvelle string, on relance la recherche
"""

