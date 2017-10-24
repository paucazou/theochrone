#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import Levenshtein
import re

def token_fuzzer(tokens,text):
    """Return the ratio for a list of tokens
    againt text.
    tokens : list of str
    text : str
    return an int as ratio, between 0 to 100"""
    tokens = [token.lower() for token in tokens if len(token) > 2]
    token_nb = len(tokens)
    text = re.sub("""[\.,;?:!"]""","",text) 
    text = re.sub("""[-']""",' ',text)
    text = [word for word in text.lower().split() if len(word) > 2 ]
    ratio = 0
    for token in tokens:
        token_ratio = 0
        for word in text:
            word_ratio = Levenshtein.ratio(token,word)
            if word_ratio > token_ratio:
                token_ratio = word_ratio
            if word_ratio == 100:
                break
        ratio += token_ratio
    return ratio / token_nb

            

