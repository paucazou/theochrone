#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the State object,
which represents the state of the central
widget of the main window"""

import calendar
import datetime
import PyQt5.QtCore as QC

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
        kwargs['parent'] = self.parent
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



    def _year(self,val: int):
        """Change the value of the year research.
        if negative, val set years before, if positive
        years after."""
        options = {
                "year"      : self.tabPlus.yy_spinbox,
                "month"     : self.tabPlus.my_spinbox,
                "week"      : self.tabPlus.wy_spinbox,
                }

        year_box = options[self.span]
        year_box.setValue(self.start.year + val)

    def _month(self,val: int):
        """Change the value of the month research
        val negative: month before
        val positive: month after
        """
        self.tabPlus.my_spinbox.setValue(self.start.year)
        options = {
                "month"     : self.tabPlus.month_combo,
                "week"      : self.tabPlus.monthweek_combo,
                }
        month_box = options[self.span] # combo_value 0..11
        month = self.start.month # month 1..12

        if month == 1 and val < 0:
            self._year(val)
            month_box.setCurrentIndex(11)
        elif month == 12 and val > 0:
            self._year(val)
            month_box.setCurrentIndex(0)
        else:
            month_box.setCurrentIndex(month-1 + val)

    def _arbitrary(self,val: int):
        """Change the dates of the arbitrary group box.
        The span is deduced by the number of days between
        start and end."""

        start = QC.QDate(self.start)
        end = QC.QDate(self.end)
        span = (start.daysTo(end)+1) * val
        #set values
        if val < 0: # why ? because the box doesn't allow 'frome' to be superior to 'to' and vice versa...
            self.tabPlus.frome.setDate(start.addDays(span))
            self.tabPlus.to.setDate(end.addDays(span))
        else:
            self.tabPlus.to.setDate(end.addDays(span))
            self.tabPlus.frome.setDate(start.addDays(span))

    def _day(self,val: int):
        """Set next or previous day."""
        base_date = QC.QDate(self.start)
        new_date = base_date.addDays(val)

        self.parent.W.onglets.W.tab1.cal.setSelectedDate(new_date)
        self.reload()

    def _week(self,val: int):
        """Set next or previous week"""
        #reset year, month and week if the are not correctly set
        self.tabPlus.wy_spinbox.setValue(self.start.year)
        self.tabPlus.monthweek_combo.setCurrentIndex(self.start.month-1)
        self.tabPlus.week_combo.setCurrentIndex(self.weeknb)

        if self.weeknb == 0 and val < 0 or self.weeknb == self.tabPlus.week_combo.count() - 1 and val > 0:
            self._month(val)
            if val < 0:
                self.tabPlus.week_combo.setCurrentIndex(
                        self.tabPlus.week_combo.count() - 1)
        else:
            self.tabPlus.week_combo.setCurrentIndex(self.weeknb + val)



    def _shift(self,val: int):
        """Called by next of previous. Set the next if
        val is positive, previous if val is negative."""
        self.tabPlus = self.parent.W.onglets.W.tabPlus # useful for functions called after
        if self.type == "kw" or self.type == 'martyrology' and self.kw:
            return
        options = {
                "year"      : self._year,
                "month"     : self._month,
                "arbitrary" : self._arbitrary,
                "day"       : self._day,
                "week"      : self._week,
                }
        res=options.get(self.span,lambda x:None)(val)
        self.reload()

    def next(self):
        """Changes the instance to the next item,
        if possible."""
        self._shift(1)

    def previous(self):
        """Changes the instance to the previous item,
        if possible"""
        self._shift(-1)

    def resetOptions(self):
        """Reset options, in the case
        they were changed"""
        ## proper
        if "proper" in self.__dict__:
            self.parent.W.mainToolbar.selectProper.setCurrentText(self.parent.propersDict[self.proper])
        ## pal
        if "pal" in self.__dict__:
            self.parent.pal.setChecked(self.pal)
        ## martyrology
        isMartyrology = self.type == "martyrology"
        self.parent.martyrology_box.setChecked(isMartyrology)

    def reload(self):
        """Reloads the central Widget"""
        # reset options if they were changed
        self.resetOptions()
        # TODO delete central widget ? Some problem occurs with garbage collector: a retranslateUI is requested for a child whose parent has already been deleted, and the child canno't get the lang, as the parent does no more exist.
        if self.type == 'kw' or self.type == "martyrology" and self.kw:
            return

        options = {
                "week"      : self.parent.useWeek,
                "month"     : self.parent.useMonth,
                "year"      : self.parent.useYear,
                "arbitrary" : self.parent.useArbitrary,
                "day"       : self.parent.useDate,
                } 

        options.get(self.span,lambda :None)()
