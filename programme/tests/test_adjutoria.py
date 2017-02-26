#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import datetime, os, sys

chemin = os.path.dirname(os.path.abspath(__file__)) + '/../'
os.chdir(chemin)
sys.path.append('.')
print(os.path.realpath('.'))

from adjutoria import datevalable

def test_datevalable():
   assert datevalable(['12022015']) == (datetime.date(2015,2,12), False, False, False)


