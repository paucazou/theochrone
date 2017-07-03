#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""A file to test officia functions"""

import calendar
import datetime
import dossier
import os
import pytest
import random
import subprocess
import unittest.mock as mock
dossier.main()

from officia import datevalable, dimancheapres, dimancheavant, mois, weekyear

def test_datevalable():
    # add more tests for this one
    # date : DDMMYYYY
    assert datevalable(['12022015']) == (datetime.date(2015,2,12), False, False, False)
    # date : (D)D (M)M
    for month in (1,3,5,7,8,10,12):
        for day in range(1,31):
            assert datevalable([str(day),str(month)]) == (datetime.date(datetime.date.today().year,month,day), False, False, False)
    for month in (4,6,9,11):
        for day in range(1,30):
            assert datevalable([str(day),str(month)]) == (datetime.date(datetime.date.today().year,month,day), False, False, False)
    for day in range(1,28):
            assert datevalable([str(day),'2']) == (datetime.date(datetime.date.today().year,2,day), False, False, False)
    # date : (D)D (M)M YYYY
    for month in (1,3,5,7,8,10,12):
        for day in range(1,31):
            assert datevalable([str(day),str(month),'2015']) == (datetime.date(2015,month,day), False, False, False)
    for month in (4,6,9,11):
        for day in range(1,30):
            assert datevalable([str(day),str(month),'2015']) == (datetime.date(2015,month,day), False, False, False)
    for day in range(1,28):
            assert datevalable([str(day),'2','2015']) == (datetime.date(2015,2,day), False, False, False)
            
    # in french only
    lang = 'francais'
    
    assert datevalable(['demain'],lang)[0] == datetime.date.today() + datetime.timedelta(1)
    assert datevalable(['hier'],lang)[0] == datetime.date.today() - datetime.timedelta(1)
    assert datevalable(['hier','avant'],lang)[0] == datetime.date.today() - datetime.timedelta(2)
    assert datevalable(['avant','hier'],lang)[0] == datetime.date.today() - datetime.timedelta(2)
    assert datevalable(['après','demain'],lang)[0] == datetime.date.today() + datetime.timedelta(2)
    assert datevalable(['demain','apres'],lang)[0] == datetime.date.today() + datetime.timedelta(2)
    
    
    liturgiccal=calendar.Calendar(firstweekday=6)
    for week in liturgiccal.monthdatescalendar(datetime.date.today().year,datetime.date.today().month):
        if datetime.date.today() in week:
            first_weekday = week[0] + datetime.timedelta(0)
    assert datevalable(['semaine'],lang) == (first_weekday, True, False, False)
    for week in liturgiccal.monthdatescalendar(datetime.date.today().year,datetime.date.today().month):
        if datetime.date.today() in week:
            first_weekday = week[0] + datetime.timedelta(7)
    assert datevalable(['semaine','prochaine'],lang) == (first_weekday, True, False, False)
    assert datevalable(['prochaine','semaine'],lang) == (first_weekday, True, False, False)
    for week in liturgiccal.monthdatescalendar(datetime.date.today().year,datetime.date.today().month):
        if datetime.date.today() in week:
            first_weekday = week[0] + datetime.timedelta(-7)
    assert datevalable(['semaine','dernière'],lang) == (first_weekday, True, False, False)
    assert datevalable(['derniere','semaine'],lang) == (first_weekday, True, False, False)
        

@mock.patch('officia.datetime')
def test_datevalable_with_patch(date_patch):
    class NewDate(datetime.date):
        year = 1960
        month = 1
        day = 1
        @classmethod
        def today(cls):
            return cls(cls.year,cls.month,cls.day)
    date_patch.date = NewDate
    
    #french
    lang = 'francais'
    for i in range(1,12):
        date_patch.date.month = i
        assert datevalable(['mois','prochain'],lang) == datevalable(['prochain','mois'],lang) == (datetime.date(1960,i + 1,1),False,True,False)
    date_patch.date.month = 12
    assert datevalable(['mois','prochain'],lang) == datevalable(['prochain','mois'],lang) == (datetime.date(1961,1,1),False,True,False)
        
        
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

@mock.patch('officia.erreur')        
def test_weekyear_iso(mock_erreur):
    """Tests wether weeks found by weekyear match with isocalendar"""
    year = random.randrange(1600,4100)
    weeknb = weekyear(year)
    for i in range(1,weeknb):
        two = weekyear(year,i)[0] + datetime.timedelta(1)
        last = weekyear(year,i)[1]
        assert two.isocalendar()[1] == last.isocalendar()[1] == i
    weekyear(2016,-1)
    weekyear(2016,53)
    assert mock_erreur.call_count == 2
        
