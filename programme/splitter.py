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

def best_match(i,string,wordcost,maxword,cost):
    """Find the best match.
    Return a (match_cost,match_length)"""
    candidates = enumerate(reversed(cost[max(0,i-maxword):i]))
    return min((c + wordcost.get(string[i-k-1:i],9e999),k+1)
            for k,c in candidates)

def infer_spaces(string,words,wordcost,maxword): # TODO essayer de deviner les mots avec Levenshtein, pour les approximations (une troisième passe)
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
