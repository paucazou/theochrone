#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module tries to split words according
to a dictionary of words frequency"""
# help : https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
from math import log

def build_cost_dic(dic): # TEST
    """Takes a dict with words as keys,
    frequency as value and return
    words (list), wordcost {word:wordcost} and word with maxlength
    """
    words = [key for key in sorted(dic,key=dic.get,reverse=True)]
    wordcost = dict((key, log((i+1) * log(len(words)))) for i, key in enumerate(words))
    maxword = max(len(x) for x in words)
    return words, wordcost, maxword

def best_match(i,string,wordcost,maxword,cost): # TEST
    """Find the best match.
    Return a (match_cost,match_length)"""
    candidates = enumerate(reversed(cost[max(0,i-maxword):i]))
    return min((c + wordcost.get(string[i-k-1:i],9e999),k+1)
            for k,c in candidates)

def infer_spaces(string,words,wordcost,maxword): # TEST
    """Infer the location of spaces from string,
    without spaces, according to a specific
    dictionary : words (simple list of words),
    wordcost : dict(word : wordcost)
    maxword : max length of word in words
    return a string"""
    # building cost array
    if string in words:
        return string
    cost = [0]
    for i in range(1,len(string) + 1):
        c,k = best_match(i,string,wordcost,maxword,cost)
        cost.append(c)

    # recover minimal-cost string
    out = []
    i = len(string)
    while i > 0:
        c,k = best_match(i,string,wordcost,maxword,cost)
        assert c == cost[i]
        out.append(string[i-k:i])
        i -= k
    
    # trying to prevent some common errors
    if not [ elt for elt in out if len(elt) > 2 ]:
        return string

    return " ".join(reversed(out))

def fuzzer_infer(string,words,min_ratio=0.85): # or 0.80 ?
    """Try to infer spaces with approximate string
    entered like "saiinjohn" (supposed to be "saint john")
    words is a iterable of words
    min_ratio is the minimum for a word to be taken"""
    from fuzzywuzzy.fuzz import partial_ratio # TODO recreate this function
    
    import Levenshtein
    
    first_wave = {word:partial_ratio(word,string) for word in words if partial_ratio(word,string) > min_ratio*100} # select all words matching with string
    
    print(first_wave)
    second_wave = {} # select only best word matching with others in the list
    deprecated_words = []
    for word in first_wave:
        if word in deprecated_words:
            continue
        matching_words = [word2 for word2 in first_wave if Levenshtein.ratio(word,word2) > 0.80]
        matching_words=sorted( matching_words,key=lambda x: first_wave[x],reverse=True)
        best_word = matching_words.pop(0)
        second_wave[best_word] = first_wave[best_word]
        deprecated_words.extend(matching_words)
        
    result = " ".join(second_wave)
    #if len(result) > len(string) # la len result doit être comprise entre 70 et 130% max (à moduler)
    # comment faire en sorte de présenter ensuite la suite la plus probable ? Trouver les combinaisons de mots qui tiennent dans l'écart (70 - 130)
    # faire passer un test à chaque combinaison proposée
    return result
        
    
