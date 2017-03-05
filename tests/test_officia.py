#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""A file to test officia functions"""

import datetime
import dossier
import subprocess
dossier.main()

from officia import datevalable, paques

def test_datevalable():
   assert datevalable(['12022015']) == (datetime.date(2015,2,12), False, False, False)
   
def test_paques():
    """ WARNING This function is a test using a french format of date.""" #faire un refus si pas possible changer
    if 'fr' not in subprocess.run(['printenv','LANG'],stdout=subprocess.PIPE).stdout.decode():
        return "Impossible to pass this test : please set your language to FR"
    passenger = datetime.datetime.today()
    for year in range(1600,4101):
        easter = subprocess.run(['ncal','-e',str(year)],stdout=subprocess.PIPE)
        easter = passenger.strptime(easter.stdout.decode(),'%d/%m/%Y\n')
        assert paques(year) == easter.date()
    
