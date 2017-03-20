#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""A file to test officia functions"""

import datetime
import dossier
import os
import random
import subprocess
dossier.main()

from officia import datevalable, dimancheapres, dimancheavant, mois, weekyear

def test_datevalable():
    # add more tests for this one
   assert datevalable(['12022015']) == (datetime.date(2015,2,12), False, False, False)
    
def test_dimancheavant():
    for i in range(1,30):
        baseday = datetime.date(1900,1,i)
        supposed_sunday = dimancheavant(baseday)
        assert supposed_sunday < baseday and supposed_sunday.weekday() == 6 and baseday - supposed_sunday <= datetime.timedelta(7)
        
def test_dimancheapres():
    for i in range(1,30):
        baseday = datetime.date(1900,1,i)
        supposed_sunday = dimancheapres(baseday)
        assert supposed_sunday > baseday and supposed_sunday.weekday() == 6 and supposed_sunday - baseday<= datetime.timedelta(7)
        
def test_weekyear():
    for year in range(1600,4101):
        yearnb = weekyear(year)
        first, last = weekyear(year, yearnb)
        sylvester = datetime.date(year,12,31)
        assert sylvester >= first and sylvester <= last
        
def test_weekyear_iso():
    """Tests wether weeks found by weekyear match with isocalendar"""
    year = random.randrange(1600,4100)
    weeknb = weekyear(year)
    for i in range(1,weeknb):
        two = weekyear(year,i)[0] + datetime.timedelta(1)
        last = weekyear(year,i)[1]
        assert two.isocalendar()[1] == last.isocalendar()[1] == i
        
