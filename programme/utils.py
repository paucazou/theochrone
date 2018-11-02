#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""Contains utilities"""

def full_of(elt,iterable)-> bool:
    """check that iterable
    is full of elt.
    if it is, return True,
    else False"""
    for item in iterable:
        if item != elt:
            return False

    return True

def valuable_length(iterable) -> int:
    """Return the length of an iterable
    after removing the elements evaluated
    to False
    >>> valuable_length(["ok","no","","else"])
    3
    """
    return len([elt for elt in iterable if elt])

def greater_valuable(f,s) -> int:
    """Takes two iterables and look
    which one has the greatest length
    and return it
    """
    return __compare_valuable(f,s,True)

def lower_valuable(f,s) -> int:
    """Similar to greater_valuable
    but return the lower one
    """
    return __compare_valuable(f,s,False)

def __compare_valuable(f,s,greater=True) -> int:
    """Base function for greater and
    lower valuable."""
    flen = valuable_length(f)
    slen = valuable_length(s)
    comparison = flen.__gt__ if greater else flen.__lt__

    if comparison(slen):
        return flen
    else:
        return slen
