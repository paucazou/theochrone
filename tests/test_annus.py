#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import easter_dates
import datetime
import dossier
import os
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
    L(1960)
    assert datetime.date(1962,3,3) in L
    assert 1962 in L
    for i in range(1600,1962):
        assert i not in L
    for i in range(1963,4100):
        assert i not in L
