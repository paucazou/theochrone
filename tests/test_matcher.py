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
import matcher

tokens = 'Maglor, le meilleur chanteur noldo'.split()

def test_is_score_low():
    m=matcher.Matcher(tokens,'en')
    assert m.is_score_low() == True
    m._best_score = { key:1 for key in m._best_score}
    m._best_score['maglor'] = 0
    assert m.is_score_low() == True
    m._best_score['maglor'] = 0.84
    assert m.is_score_low() == True
    assert m.is_score_low(floor=0.83) == False
    
def test_reset_scores():
    m=matcher.Matcher(tokens,'en')
    m._best_score = { key:0.8 for key in m._best_score}
    m.reset_scores()
    assert max(m._best_score.values()) == 0
