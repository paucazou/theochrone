#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""This module provides way to output
correct dates in requested language"""

languages_available = {'fr','en','la'}

months = {'fr':('','janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'),
          'la':('','Januarii', 'Februarii', 'Martii', 'Aprilis', 'Maii', 'Junii', 'Julii', 'Augusti', 'Septembtis', 'Octobris', 'Novembris', 'Decembris')
          }

def main(lang,item,item_type):
    """This function returns the
    returned value of function matching 
    lang
    item is a datetime like obj to render
    item_type is if item is a day, a month, etc."""
    functions = {'fr':_fr,'la':_la}
    if lang not in languages_available:
        raise ValueError("Language requested is not available")
    return functions[lang](item,item_type)

def _fr(item,item_type):
    """For french"""
    if item_type == "day":
        if item == 1:
            item = "1er"
        item = str(item)
    return item

def _la(item,item_type):
    """For latin"""
    return str(item)

