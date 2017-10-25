#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import Levenshtein
import phlog
import re

logger = phlog.loggers['console']

def token_fuzzer(tokens,text):
    """Return the ratio for a list of tokens
    againt text.
    tokens : list of str
    text : str
    return an int as ratio, between 0 to 100"""
    tokens = {token.lower() for token in tokens if len(token) > 2}
    token_pos = { token: {'index':0,'score':0} for token in tokens }
    token_nb = len(tokens)
    text = re.sub("""[\.,;?:!"]""","",text) 
    text = re.sub("""[-']""",' ',text)
    text = [word for word in text.lower().split() if len(word) > 2 ]
    ratio = 0
    for token in tokens:
        token_ratio = 0
        for index, word in enumerate(text):
            word_ratio = Levenshtein.ratio(token,word)
            if word_ratio > token_ratio:
                token_ratio = word_ratio
                token_pos[token]['index'] = index
                token_pos[token]['score'] = token_ratio
            if word_ratio == 1:
                break
        ratio += token_ratio
    distance_ratio = word_distance(token_pos,token_nb)
    fuzz_ratio = ratio / token_nb
    
    if fuzz_ratio > 0.85 and distance_ratio >= 0.0001:
        logger.debug('{} : {}'.format(tokens,text))
    return fuzz_ratio - distance_ratio

def word_distance(token_pos,token_nb):
    """Takes token_pos dict, the number of tokens (token_nb)
    and return the distance ratio :
    if ratio is equal to token_nb = 0
    The distance ratio is very low, for it is just intended to discriminate
    equal high results"""
    if token_nb == 1: # case of an only token
        return 0
    
    values = tuple(value['index'] for value in sorted(token_pos.values(),key=lambda x:x['index']) if value['score'] > 0.85)
    if not values:
        return 0
    
    raw_distance = max(values) - min(values) + 1 # problème à prévoir avec l'index 0 ?
    #logger.debug("raw_distance : {}".format(raw_distance))
    
    # managing the case of a token which has a score lower than 0.85
    len_diff = token_nb - len(values)
    #logger.debug("len_diff : {}".format(len_diff))
    len_diff = (-len_diff,len_diff)[raw_distance > token_nb]
    #logger.debug('new len_diff : {}'.format(len_diff))
    
    mod_distance = raw_distance + len_diff
    distance_ratio = abs((mod_distance/token_nb -1) * 0.00001)
    
    return distance_ratio



"""
au cas où un mot n'ait pas atteint le score de 0.5 une seule fois :
on fait appel à word_frequency (changer ce nom inadapté), et, en cas de nouvelle string, on relance la recherche
"""

