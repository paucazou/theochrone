#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""A file to test officia functions"""

import datetime
import dossier
import os
import subprocess
dossier.main()

from officia import datevalable, dimancheapres, dimancheavant, mois, paques, weekyear

def test_datevalable():
    # add more tests for this one
   assert datevalable(['12022015']) == (datetime.date(2015,2,12), False, False, False)
   
def test_paques():
    """ WARNING This function is a test using a french format of date.""" #faire un refus si pas possible changer
    os.environ['LANG'] = "fr_FR.UTF-8"
    firstest = subprocess.run(['ncal','-e','1962'],stdout=subprocess.PIPE).stdout.decode()
    if firstest == '22/04/1962\n':
        strformat = '%d/%m/%Y\n'
        month_letter = False
    elif firstest == '22 avril 1962\n':
        strformat = '%d/%m/%Y'
        month_letter = True
    else:
        return False # impossible to pass the test
    passenger = datetime.datetime.today()
    for year in range(1600,4101):
        easter = subprocess.run(['ncal','-e',str(year)],stdout=subprocess.PIPE)
        if month_letter:
            easter = easter.split()
            if easter[1] == 'avril':
                easter[1] = '04'
            else:
                easter[1] = '03'
            easter = '/'.join(easter)
        easter = passenger.strptime(easter.stdout.decode(),strformat)
        assert paques(year) == easter.date()
    
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
        
def test_weekyear(): # faire un autre test basé sur isocalendar
    for year in range(1600,4101):
        yearnb = weekyear(year)
        first, last = weekyear(year, yearnb)
        sylvester = datetime.date(year,12,31)
        assert sylvester >= first and sylvester <= last
        
