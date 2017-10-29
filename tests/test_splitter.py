#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import datetime
import copy
import dossier
import os
import pytest
import random
import unittest.mock as mock

dossier.main()
import splitter

example = {'maglor':55,'maedhros':100,'curufin':140,'caranthir':155,'celegorm':200,'amrod':245,'amras':300}

example_cost_dic = (['amras', 'amrod', 'celegorm', 'caranthir', 'curufin', 'maedhros', 'maglor'],
 {'amras': 0.6657298105782764,
  'amrod': 1.3588769911382217,
  'caranthir': 2.052024171698167,
  'celegorm': 1.764342099246386,
  'curufin': 2.275167723012377,
  'maedhros': 2.4574892798063313,
  'maglor': 2.6116399596335897},
 9)


def test_build_cost_dic():
    result = splitter.build_cost_dic(example)
    assert isinstance(result,tuple)
    assert len(result) == 3
    words, wordcost, maxword = result
    assert maxword == len('caranthir')
    assert words == ['amras', 'amrod', 'celegorm', 'caranthir', 'curufin', 'maedhros', 'maglor']
    assert wordcost == {'amrod': 1.3588769911382217, 'maedhros': 2.4574892798063313, 'amras': 0.6657298105782764, 'maglor': 2.6116399596335897, 'caranthir': 2.052024171698167, 'curufin': 2.275167723012377, 'celegorm': 1.764342099246386}
    
def test_best_match(): # Not sure to really understand how this function works...
    word_cost, maxword = example_cost_dic[1:]
    assert splitter.best_match(1,'caranthiramras',word_cost,maxword,[0]) == (float('inf'),1)
    
def test_infer_spaces():
    string = 'celegorm'
    assert splitter.infer_spaces(string,*example_cost_dic) == string
    
    string = "celegormcaranthircurufin"
    assert splitter.infer_spaces(string,*example_cost_dic) == "celegorm caranthir curufin"
    
    ncostdict = (['rr', 'ha', 'r', 'd', 'amras', 'amrod', 'celegorm', 'caranthir', 'curufin', 'maedhros', 'maglor'], {'amrod': 2.666350852151744, 'caranthir': 2.954032924603525, 'amras': 2.4840292953577894, 'ha': 1.5677385634836343, 'd': 2.2608857440435797, 'maedhros': 3.1771764759177348, 'rr': 0.874591382923689, 'maglor': 3.2724866557220595, 'celegorm': 2.8205015319790023, 'curufin': 3.0718159602599084, 'r': 1.9732036715917987}, 9)
    
    string = "rrha"
    assert splitter.infer_spaces(string,*ncostdict) == string
    
    
    
