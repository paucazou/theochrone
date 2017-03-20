#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import datetime
import dossier
import os
import subprocess

dossier.main()
import annus

L = annus.LiturgicalYear()


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
        assert L.easter(year) == easter.date()
