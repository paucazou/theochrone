#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Contains a wrapper to humanize the presentation
of a Fete object"""

import datetime
import messages
import os


def toEmptyString(fun):
    """Decorator. The function defined
    returns an empty string ('') if returned
    value is evaluated to False (None, '', 0...)
    Same if an error occured, like IndexError or KeyError
    """
    def wrapper(*args,**kwargs):
        """Wrapper of the function decorated"""
        try:
            res = fun(*args,**kwargs)
        except (KeyError,IndexError):
            res = None
        return res if res else ''

    return wrapper

class FeastWrapper:
    """Return informations more readable by humans"""

    def __init__(self,feast,lang='en'):
        """Inits the object.
        feast is an adjutoria.Fete object,
        or one of its children.
        It must be already set, i.e. it must have a specific date and a parent.
        lang must be set: only one wrapper by language"""
        if feast.parent is None or feast.date is None:
            raise ValueError("Feast is not already set: {}".format(feast))
        self.feast = feast
        self.lang = lang
        #translations
        type(self).msg = messages.translated_messages('feastprinter',lang)


    def __str__(self):
        return "FeastWrapper: {}".format(self.feast)

    __repr__ = __str__

    # class methods
    @classmethod
    def humandate(cls,date: datetime.date,lang='en',weekday=False) -> str:
        """Return a humanized and localized date
        for requested lang. If weekday is set, return the weekday too"""
        weekday_string = {'en':"{}, ",
                'fr':"{} "}
        actual_weekday = weekday_string[lang].format(cls.msg.weekdays[date.weekday()]) if weekday else ''
        month = cls.msg.months[date.month]
        if lang == 'fr':
            day_nb = date.day if date.day > 1 else '1er'
            return "{}{} {} {}".format(
                    actual_weekday,
                    day_nb,month,date.year)
        else: # en
            return "{}{} {}, {}".format(
                actual_weekday,
                month,date.day,date.year)

    ## getters

    @toEmptyString
    def _get_addendum(self):
        """Return the addendum for
        the lang requested"""
        return self.feast.addendum.get(self.lang)

    @toEmptyString
    def _get_class(self):
        """Return the class of the feast
        as a localized string"""
        return self.msg.classes[self.feast.degre]

    def _get_color(self):
        """Return the liturgical colour
        for the feast as a localized string"""
        return self.msg.colors[self.feast.couleur]

    def _get_date(self):
        """Return the date of the feast
        as a humanized and localized string"""
        return self.humandate(self.feast.date,self.lang)

    def _get_digitdate(self):
        """Return the date as a set of digits
        splitted by /"""
        formats = {
                'fr':'{2}/{1}/{0}',
                'en':'{1}/{2}/{0}',
                }
        return formats[self.lang].format(
                self.feast.date.year,
                self.feast.date.month,
                self.feast.date.day)

    def _get_edition(self):
        """Return the edition date of the feast
        selected"""
        return self.feast.ordo

    def _get_fulldate(self):
        """Return the date of the feast
        with the weekday"""
        return self.humandate(self.feast.date,self.lang,weekday=True)

    def _get_name(self):
        """Return the name of the feast
        for requested lang"""
        return self.feast.nom[self.lang] # an error must be raised if name canno't be found for lang

    def _get_pal(self):
        """If a feast is Pro Aliquibus locis, return
        a string mentioning it.
        If not return ''"""
        return self.msg.pal if self.feast.pal else '' 

    def _get_proper(self):
        """Return the proper as a humanized
        and localized string"""
        return self.msg.propers[self.feast.propre]

    def _get_season(self):
        """Return the liturgical time"""
        return self.msg.seasons[self.feast.temps_liturgique()]

    @toEmptyString
    def _get_station(self):
        """Return station if there is one"""
        if getattr(self.feast,'station',False):
            return self.feast.station.get(self.lang,'')

    def _get_status(self):
        """Return the status of the feast"""
        if self.feast.celebree:
            return self.msg.celebrated
        if self.feast.peut_etre_celebree and self.feast.commemoraison:
            return self.msg.celebrated_commemorated
        if self.feast.peut_etre_celebree and not self.feast.commemoraison:
            return self.msg.can_celebrated
        if self.feast.commemoraison:
            return self.msg.commemorated
        if self.feast.omission:
            return self.msg.omitted

    @toEmptyString
    def _get_temporsanct(self):
        """Return if a feast is of the Sanctoral
        or Temporal"""
        if self.feast.temporal:
            return self.msg.temporal
        elif self.feast.sanctoral:
            return self.msg.sanctoral

    @toEmptyString
    def _get_transfert(self):
        """Return if the feast is transferred,
        and from which date"""
        if self.feast.transferee:
            return self.msg.transfert.format(
                    self.humandate(self.feast.date_originelle,self.lang)
                    )

    def _get_weekday(self):
        """Return the weekday of the feast"""
        return self.msg.weekdays[self.feast.date.weekday()]

    ## properties
    addendum = property(_get_addendum)
    Class = property(_get_class) # uppercase, because class is a keyword
    color = property(_get_color)
    date = property(_get_date)
    digitdate = property(_get_digitdate)
    edition = property(_get_edition)
    fulldate = property(_get_fulldate) # with weekday
    name = property(_get_name)
    pal = property(_get_pal)
    proper = property(_get_proper)
    season = property(_get_season)
    station = property(_get_station)
    status = property(_get_status)
    temporsanct = property(_get_temporsanct)
    transfert = property(_get_transfert) # may return '' or 'transferred from DATE'
    weekday = property(_get_weekday)

