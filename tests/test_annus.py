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


L = annus.LiturgicalCalendar()


def test_paques():
    """A function to test every easter date from 1600 to 4100"""
    for year in range(1600,4100):
        assert L.easter(year) == easter_dates.check_dates[year]
        
        
        
