#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Contains a wrapper to humanize the presentation
of a Fete object"""

import datetime
import gettext
import os

loc = os.path.dirname(os.path.abspath(__file__)) + '/../i18n'


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
    weekdays_translated = (
        _('Monday'),_('Tuesday'),_('Wednesday'),
        _('Thursday'),_('Friday'),_('Saturday'),_('Sunday'))
    lang_installed = 'en'
    translation_installed = None

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
        # install translations
        if lang != self.lang_installed:
            self.translation_installed = gettext.translation('feastprinter',loc,languages=[lang],fallback=True)
            self.translation_installed.install()

    def __str__(self):
        return "FeastWrapper: {}".format(self.feast)

    __repr__ = __str__

    # class methods
    @classmethod
    def humandate(cls,date: datetime.date,lang='en',weekday=False) -> str:
        """Return a humanized and localized date
        for requested lang. If weekday is set, return the weekday too"""
        months = ('',_('January'),_('February'),_('March'),
                _('April'),_('May'),_('June'),_('July'),
                _('August'),_('September'),_('November'),_('December'))
        weekday_string = {'en':"{}, ",
                'fr':"{} "}
        actual_weekday = weekday_string[lang].format(cls.weekdays_translated[date.weekday()]) if weekday else ''
        month = months[date.month]
        if lang == 'fr':
            day_nb = date.day if date.day > 1 else '1er'
            return "{}{} {} {}".format(
                    actual_weekday,
                    day_nb,month,date.year)
        else: # en
            return "{}{} {}, {}".format(
                actual_weekday,
                date.month,date.day,date.year)

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
        classes = ('',_("First class"),
                _("Second class"),
                _("Third class"),
                _("Fourth class"),
                _("Commemoration")) # Pro aliquibus locis is not here, but in _get_pal
        return classes[self.feast.degre]

    def _get_color(self):
        """Return the liturgical colour
        for the feast as a localized string"""
        colors = {
                'blanc':_('white'),
                'noir':_('black'),
                'rouge':_('red'),
                'vert':_('green'),
                'violet':_('violet'),
                }
        return colors[self.feast.couleur]

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
        return _("Mass Pro Aliquibus Locis") if self.feast.pal else '' 

    def _get_proper(self):
        """Return the proper as a humanized
        and localized string"""
        propers = {
                'roman'         :_('Roman'),
                'australian'    :_('Australian'),
                'brazilian'     :_('Brazilian'),
                'canadian'      :_('Canadian'),
                'english'       :_('English'),
                'french'        :_('French'),
                'new_zealander' :_('New-Zealander'),
                'polish'        :_('Polish'),
                'portuguese'    :_('Portuguese'),
                'scottish'      :_('Scottish'),
                'spanish'       :_('Spanish'),
                'welsh'         :_('Welsh')
                }
        return propers[self.feast.propre]

    def _get_season(self):
        """Return the liturgical time"""
        seasons = {
                'avent'             :_("Season of Advent"),
                'nativite'          :_("Christmastide (Season of Christmas)"),
                'epiphanie'         :_("Epiphanytide (Season of Christmas)"),
                'apres_epiphanie'   :_("Season per annum after Epiphany"),
                'septuagesime'      :_("Season of Septuagesim"),
                'careme'            :_("Lent (Season of Lent)"),
                'passion'           :_("Passiontide (Season of Lent)"),
                'paques'            :_("Eastertide (Season of Easter)"),
                'ascension'         :_("Ascensiontide (Season of Easter)"),
                'octave_pentecote'  :_("Octave of Pentecost (Season of Easter)"),
                'pentecote'         :_("Season per annum after Pentecost"),
                }
        return seasons[self.feast.temps_liturgique()]

    @toEmptyString
    def _get_station(self):
        """Return station if there is one"""
        if getattr(self.feast,'station',False):
            return self.feast.station.get(self.lang,'')

    def _get_status(self):
        """Return the status of the feast"""
        if self.feast.celebree:
            return _("celebrated")
        if self.feast.peut_etre_celebree and self.feast.commemoraison:
            return _("can be celebrated or commemorated")
        if self.feast.peut_etre_celebree and not self.feast.commemoraison:
            return _("can be celebrated")
        if self.feast.commemoraison:
            return _("commemorated")
        if self.feast.omission:
            return _("omitted")

    @toEmptyString
    def _get_temporsanct(self):
        """Return if a feast is of the Sanctoral
        or Temporal"""
        if self.feast.temporal:
            return _("Temporal")
        elif self.feast.sanctoral:
            return _("Sanctoral")

    @toEmptyString
    def _get_transfert(self):
        """Return if the feast is transferred,
        and from which date"""
        if self.feast.transferee:
            return _("Transfered. Original date: {}").format(
                    self.humandate(self.feast.date_originelle,self.lang)
                    )

    def _get_weekday(self):
        """Return the weekday of the feast"""
        return self.weekdays_translated[self.feast.date.weekday()]

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

