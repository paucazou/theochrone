#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module parses
a xml file exported via gui of libreoffice,
from a .odt file."""

from dataswitcher import finput
import polyglot.detect as polydet
import xml.etree.ElementTree as eltree
import lxml.etree

no_error_parser = lxml.etree.XMLParser(recover = True)


def _detect_language(string):
    """Detects language and returned code 
    as following : 'la','fr'.
    If automatic detection can't be made,
    user input is required"""
    string_detector = polydet.Detector(string)
    if string_detector.language.confidence < 90 or not string_detector.reliable:
        answer = ''
        if 'En lune de...' in string:
            answer = 'fr'
        elif 'Die' in string and string.count('†') == 2:
            answer = 'la'
        while answer not in ('la','fr'):
            print(string)
            suggestion = ['',string_detector.language.code][string_detector.language.code in ('la','fr')]
            answer = finput("Quelle est la langue de ce passage ? fr/la\n",suggestion)
        return answer
    return string_detector.language.code

def _get_children(root,martyrology):
    """Recursive function.
    Get children of root"""
    if root.tag == "text":
        martyrology = _process_text(root.text,martyrology)
    elif root.tag in ('infos','Text','LineBreak','Special'):
        return martyrology
    else:
        for child in root:
            martyrology = _get_children(root,martyrology)
    return martyrology

def _process_text(text,martyrology):
    """Check language of text.
    Check if it is a new day,
    and create it if necessary
    put it in the martyrology dict
    return martyrology dict modified"""
    l_code = _detect_language(text)
    if l_code == 'la':
        if '† Die ' in text:
            martyrology['la'].append('')
        martyrology['la'][-1] += text
    elif l_code == 'fr':
        if 'En lune de...' in text:
            martyrology['fr'].append('')
        martyrology['fr'][-1] += text
    return martyrology
        
def parse_data(path):
    """Parse data from path
    return two lists, one for latin, one for french.
    Each list[0] == 28th of Nov"""
    martyrology = {'la':[],'fr':[]}
    tree = eltree.parse(path,parser = no_error_parser)
    martyrology = _get_children(tree.getroot(),martyrology)
    return martyrology


