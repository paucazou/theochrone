#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import easter_dates
import datetime
import dossier
import os
import pytest
import random
import subprocess
import unittest.mock as mock

dossier.main()
import annus

class FakeFeast(mock.MagicMock):
    """A class which simulates the Fete class behaviour"""
    
    def __init__(self,
                 priorite,commemoraison_privilegiee,
                 date,personne,
                 dimanche=False,fete_du_Seigneur=False,):
        self.priorite = priorite
        self.commemoraison_privilegiee = commemoraison_privilegiee
        self.date = None
        self.date_ = date
        self.personne = personne
        
        self.dimanche = dimanche
        self.fete_du_Seigneur = fete_du_Seigneur
        
        self.peut_etre_celebree=False
        self._transferee=False
        self.date_originelle=None
        self.celebree=True
        self.omission=False
        self.commemoraison=False
        
        self.proper = 'romanus'
        self.ordo = 1962
        
    def DateCivile(self,year):
        return datetime.date(year,self.date_[0],self.date_[1])



@mock.patch("pickle.Unpickler")
@mock.patch("__main__.open")
@pytest.fixture
def send_empty_liturgical_calendar(mock_open,mock_unpickler):
    mock_load = mock.MagicMock()
    mock_load.load.return_value=[mock.MagicMock(),mock.MagicMock()]
    mock_unpickler.return_value = mock_load
    return annus.LiturgicalCalendar()

@pytest.fixture
def send_one_year_liturgical_calendar(send_empty_liturgical_calendar):
    L = send_empty_liturgical_calendar
    L(1962)
    return L

def test_paques():
    """A function to test every easter date from 1600 to 4100"""
    for year in range(1600,4100):
        assert annus.LiturgicalCalendar.easter(year) == easter_dates.check_dates[year]
        
def test_oncecalled():
    mock_class = mock.MagicMock()
    mock_class.once_called = []
    mock_class.method.return_value=True
    mock_class.method = annus.oncecalled(mock_class.method)
    assert mock_class.method(mock_class) == True
    assert mock_class.method(mock_class) == False

def test_contains(send_one_year_liturgical_calendar):
    L = send_one_year_liturgical_calendar
    assert datetime.date(1962,3,3) in L
    assert 1962 in L
    for i in range(1600,1962):
        assert i not in L
    for i in range(1963,4100):
        assert i not in L
        
def test_len(send_one_year_liturgical_calendar):
    L=send_one_year_liturgical_calendar
    assert len(L) == 1
    L(1975)
    assert len(L) == 2
    L(1975)
    assert len(L) == 2
    L(1990)
    assert len(L) == 3
    
def test_repr(send_empty_liturgical_calendar):
    assert send_empty_liturgical_calendar.__repr__(
        ) == """LiturgicalYear. {}/{}""".format(
            send_empty_liturgical_calendar.ordo,
            send_empty_liturgical_calendar.proper)
        
def test_str(send_empty_liturgical_calendar):
    L=send_empty_liturgical_calendar
    debut = random.randrange(1962,2000)
    fin = random.randrange(debut,2001)
    L(debut,fin)
    assert L.__str__() == """LiturgicalYear. Ordo : {}. Proper : {}. Years already loaded : {}.""".format(L.ordo,L.proper,", ".join(
        [str(year) for year in range(debut,fin+1)]))
        
@mock.patch("pickle.Unpickler")
@mock.patch("__main__.open")
def test_load_raw_data(mock_open,mock_unpickler):
    mock_load = mock.MagicMock()
    mock_load.load.return_value=[1,2]
    mock_unpickler.return_value = mock_load
    L = annus.LiturgicalCalendar()
    assert isinstance(getattr(L,'raw_data'),list)
    assert getattr(L,'saturday') == 1
    assert getattr(L,'feria') == 2
    for name, item in zip(annus.fichiers,mock_unpickler.call_args_list):
        assert name in item.__repr__() # pas terrible, mais on s'assure que l'appel a été fait à tous les fichiers. # TODO Tester l'existence des fichiers ?

def test_create_empty_year():
    year = random.randrange(1600,4100)
    empty_year = annus.LiturgicalCalendar.create_empty_year(year)
    date = datetime.date(year,1,1)
    while True:
        assert date in empty_year
        assert empty_year[date] == []
        date = date + datetime.timedelta(1)
        if date.year != year:
            break
        
def test_call():
    def _create_year(year):
        FakeCalendar.year_names.append(year)
        FakeCalendar.year_names.sort()
    FakeCalendar = mock.MagicMock()
    FakeCalendar.call = annus.LiturgicalCalendar.__call__
    FakeCalendar.year_names = []
    FakeCalendar._create_year = _create_year
    
    assert FakeCalendar.year_names == []
    FakeCalendar.call(FakeCalendar,1962)
    assert FakeCalendar.year_names == [1962]
    FakeCalendar.call(FakeCalendar,1962)
    assert FakeCalendar.year_names == [1962]
    FakeCalendar.call(FakeCalendar,1964,1966)
    assert FakeCalendar.year_names == [1962, 1964, 1965, 1966]
    assert FakeCalendar.call(FakeCalendar,1200) == False
    assert FakeCalendar.call(FakeCalendar,5000) == False
    assert FakeCalendar.call(FakeCalendar,1540,1700) == False
    assert FakeCalendar.call(FakeCalendar,3000,5000) == False
    assert FakeCalendar.call(FakeCalendar,2000,1995) == False
    assert FakeCalendar.year_names == [1962, 1964, 1965, 1966]
    
