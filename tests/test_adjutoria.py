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
    fete1._temps_liturgique = 'Sometimes'
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
    
def test_hash():
    fete = adjutoria.Fete()
    
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
    assert fete1 == fete2 and not(fete1 is fete2)

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
    
def test_temps_liturgique():
    fete = fete_base()
    assert fete.temps_liturgique() == 'Sometimes'
    fete._temps_liturgique = 'variable'
    fete.date = datetime.date(1962,1,1)
    fete.parent = mock.MagicMock()
    fete2 = adjutoria.Fete()
    fete2.temporal = True
    fete2._temps_liturgique = 'A time'
    fete.parent.__getitem__.return_value = [fete2]
    assert fete.temps_liturgique() == fete2._temps_liturgique
    assert mock.call(fete.date) in fete.parent.__getitem__.call_args_list
    assert fete.parent.__getitem__.call_count == 1

def test_set_transferee():
    fete = fete_base()
    fete.date = datetime.date(1962,1,1)
    assert not fete.transferee and not fete.date_originelle
    fete.transferee = True
    assert fete.transferee and fete.date_originelle == datetime.date(1962,1,1) and fete.date == datetime.date(1962,1,2)
    fete.transferee = True
    assert fete.transferee and fete.date_originelle == datetime.date(1962,1,1) and fete.date == datetime.date(1962,1,3)

@mock.patch('adjutoria.images')    
def test_get_images(images):
    images.get.return_value = None
    fete = fete_base()
    assert fete._images is '' and fete.images == fete._get_images() == None
    fete._images = "Fete"
    assert fete._images == "Fete" and fete.images == fete._get_images() == None
    images.get.return_value = True
    images.__getitem__.return_value = "Yes"
    assert fete.images == fete._get_images() == "Yes"
    assert images.__getitem__.call_count == 2 and mock.call(fete._images) in images.__getitem__.call_args_list
    
    
