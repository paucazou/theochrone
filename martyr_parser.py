#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

from dataswitcher import finput
import unicodedata
import fuzzywuzzy.fuzz as fuzz


def remove_duplicate(martyrology):
    nmartyrology = {}
    for lang, lists in martyrology.items():
        nlists = []
        print(lang)
        for j,day in enumerate(lists):
            nday = []
            day = day.split('\n')
            for i,line in enumerate(day):
                answer = 'oui'
                if line != day[-1]:
                    if fuzz.ratio(line,day[i+1]) >= 90:
                        print(j)
                        answer = "non"
                if answer == 'oui':
                    nday.append(line)
            nlists.append('\n'.join(nday))
        nmartyrology[lang] = nlists
    return nmartyrology


def process_text(text,martyrology):
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

def _detect_language(string):
    answer = ''
    if 'En lune de...' in string:
        answer = 'fr'
    elif 'Die' in string and string.count('†') == 2:
        answer = 'la'
    else:
        if set(string.lower().split()).intersection({'saint','sainte','saintes',
                                                     'bienheureux','bienheureuse','bienheureuses','saints',
                                                     'confesseur','vierge','vierges',
                                                     'martyrs','martyrs,','martyrs.'}):
            answer = 'fr'
        if {sans_accent(word) for word in string.split()}.intersection({'sancti','sanctæ',
                                                                        'beati','beatæ',
                                                                        'sanctarum','sanctorum',
                                                                        'virginis','virginum',
                                                                        'martyrum',}):
            answer = ('la','')[answer == 'fr']
        while answer not in ('la','fr'):
            answer = finput(string + "\nQuelle est la langue de ce passage ? fr/la\n",answer)
            
    return answer
                                                     
                                                     

def sans_accent(mot): # TEST 
    """Prend des mots avec accents, cédilles, etc. et les renvoie sans, et en minuscules."""
    return ''.join(c for c in unicodedata.normalize('NFD',mot.lower()) if unicodedata.category(c) != 'Mn')
