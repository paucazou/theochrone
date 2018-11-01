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
