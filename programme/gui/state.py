#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the State object,
which represents the state of the central
widget of the main window"""

import calendar
import datetime

class State:
    """State of the central widget in a
    main window"""

    def __init__(self,parent,**kwargs):
        """Inits the object.
        parent should be a QMainWindow object.
        kwargs are passed to set the object."""
        self.parent = parent
        self.__call__(**kwargs)

    def __call__(self,**kwargs):
        """Called when state changes.
        kwargs become the attributes of the
        instance. They depend on the type of the
        central widget.
        required keys are type and data, as they
        allow the object to determine the others keys.
        No verification is made."""
        self.__dict__ = kwargs
        if kwargs.get('type',False) == 'date' and self.span != "arbitrary":
            if self.span == "day":
                lcalendar = self.data[0].parent
                self.start = self.end = self.data[0].date
            elif self.span == "week":
                week = sorted(self.data.items())
                self.start = week[0][0]
                self.end = week[-1][0]
            elif self.span == "month":
                week = sorted(self.data[(0,'week')].items())
                self.start = week[0][0]
                last_day = calendar.monthrange(self.start.year,self.start.month)[-1]
                self.end = datetime.date(self.start.year,self.start.month,last_day)
            elif self.span == "year":
                week = sorted(self.data[(1,'month')][(0,'week')].items())
                self.start = week[0][0]
                self.end = datetime.date(self.start.year,12,31)

            if self.span != 'day':
                lcalendar = week[0][1][0].parent # 0: first day, 1 the value, 0 first feast of day
            self.ordo = lcalendar.ordo
            self.proper = lcalendar.proper


    def next(self):
        """Changes the instance to the next item,
        if possible."""
        pass

    def previous(self):
        """Changes the instance to the previous item,
        if possible"""
        pass

    def reload(self):
        """Reloads the central Widget"""
        # TODO should be called in next and previous after changes ?
        pass
