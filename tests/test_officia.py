#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""A file to test officia functions"""

import datetime
import dossier
dossier.main()

from officia import datevalable

def test_datevalable():
   assert datevalable(['12022015']) == (datetime.date(2015,2,12), False, False, False)
