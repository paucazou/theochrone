#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import easter_dates
import datetime
import dossier
import os
import random
import subprocess
import unittest.mock as mock

dossier.main()
import annus


def test_paques():
    """A function to test every easter date from 1600 to 4100"""
    L = annus.LiturgicalCalendar()
    for year in range(1600,4100):
        assert L.easter(year) == easter_dates.check_dates[year]
        
def test_oncecalled():
    mock_class = mock.MagicMock()
    mock_class.once_called = []
    mock_class.method.return_value=True
    mock_class.method = annus.oncecalled(mock_class.method)
    assert mock_class.method(mock_class) == True
    assert mock_class.method(mock_class) == False

def test_contains():
    L = annus.LiturgicalCalendar()
    L(1962)
    assert datetime.date(1962,3,3) in L
    assert 1962 in L
    for i in range(1600,1962):
        assert i not in L
    for i in range(1963,4100):
        assert i not in L
        
@mock.patch("pickle.Unpickler")
@mock.patch("__main__.open")
def test_load_raw_data(mock_open,mock_pickle):
    L = annus.LiturgicalCalendar()
    assert getattr(L,'raw_data') is not None
    assert getattr(L,'saturday') is not None
    assert getattr(L,'feria') is not None # Pas terrible. Comment être sûr que l'appel à Pickle a été fait ?

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
