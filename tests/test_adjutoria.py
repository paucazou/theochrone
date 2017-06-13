#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import datetime
import os
import pytest
import sys
import dossier
import unittest.mock as mock
dossier.main()

import adjutoria

def fete_base():
    fete1 = adjutoria.Fete()
    fete1.degre = 1
    fete1._priorite = 1800
    return fete1

# Test Fete
def test_lt():
    fete1 = fete_base()
    autrefete = adjutoria.Fete()
    autrefete.degre = 3
    autrefete._priorite = 550
    assert fete1.__lt__(autrefete)
    autrefete.degre = 1
    assert fete1.__lt__(autrefete)
    
    
def test_eq():
    fete1 = fete_base()
    fete2 = fete_base()
    with pytest.raises(TypeError):
        fete1.__eq__(1)
    assert fete1.__eq__(fete2)
    fete2.valeur = 4
    assert not fete2.__eq__(fete1)

def test_copy():
    fete1 = fete_base()
    fete2 = fete1.copy()
    assert fete1 == fete2 and fete1 is not fete2

@mock.patch('adjutoria.Fete.DateCivile_')    
def test_DateCivile(DateCivile_):
    fete = fete_base()
    fete.DateCivile(datetime.date.today(),1962)
    fete.date = datetime.date.today()
    assert DateCivile_.call_count == 1
    assert mock.call(datetime.date.today(),1962) in DateCivile_.call_args_list
    
def test_paques():
    fete = fete_base()
    fete.date = datetime.date(1962,4,21)
    easter = datetime.date(1962,4,22)
    assert fete.DatePaques(easter,1962) == datetime.timedelta(1)
    
    
    

    
