#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module looks into a martyrology file
and save words by frequence in a dictionary"""

import datetime
import programme.officia
import re

def create_frequence_dico(lang,martyrology_inst):
    words_dic = {}
    bdate = datetime.date(2016,1,1)
    while bdate < datetime.date(2017,1,1):
        result = martyrology_inst.daytext(bdate,lang)
        for line in result.main:
            line = re.sub("""[\.\(\),;?:!\-'"]"""," ",line) 
            for word in line.split():
                if any(char.isdigit() for char in word):
                    continue
                word = programme.officia.sans_accent(word)
                words_dic.setdefault(word,0)
                words_dic[word] += 1
        bdate = bdate + datetime.timedelta(1)
    return words_dic



    
