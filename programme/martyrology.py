#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the Martyrology class"""

import calendar
import humandate
import os

class Martyrology:
    """The Roman Martyrology.
    This class can only contain one edition (by date)
    of the martyrology, with its different translations"""
    _first_line = {
            } # a dict of the pattern for the first line
    _last_line = {
            } # a dict of the last lines

    def __init__(self,date=1962):
        """Inits the class.
        date is the edition selected.
        Loads names of files"""
        pattern = "roman_martyrology_{}.pkl"
        files_list = [file for file in os.listdir('data') if pattern in file]
        self._data = { 
                file.split('_')[0] : file
                for file in files_list}

    def daytext(self,date,language):
        """date is a datetime.date like object.
        Return text for requested day and locale"""
        i = date.day
        if date.month == 2 and date.day >= 25 and calendar.isleap(date.year):
            i -=1
        base = self._get_data[language][i]
        day_formatted = humandate.main(language,date.day,'day')
        first_line = self._first_line[language].format(day_formatted)
        return base.format(first_line,
                self._last_line[language])

    def _get_data(self,language):
        """Loads data if necessary.
        Return self._data[language]"""
        if isinstance(self._data[language],str):
            with open(self._data[language],'br') as f:
                self._data[language] = picle.Unpickler(f).load()
        return self._data[language]

    def credits(self,language):
        """Return appropriate credits for
        requested language"""
        return self._get_data(language]['credits']

