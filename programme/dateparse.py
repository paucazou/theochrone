#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module defines classes 
which take a list of strings and return a date object"""
import calendar
import collections
import datetime
import dateutil.parser
import locale
import messages
import subprocess
import sys

msg = messages.translated_messages('dateparse')
today = datetime.date.today()
TimeSpan = collections.namedtuple('TimeSpan',('start','stop'))

class _DateParser:
    """Abstract base class"""
    def __init__(self,input: list, lang: str, input2=None):
        """Defines attributes"""
        self.input = input # --FROM
        self.input2 = input2 # --TO
        self.lang = lang
        self.today = today
        self._resolution_order = [
                (self._today,), #0
                [self._today,self._oneword], #1

                ] # a list of lists with the methods in the good order to return the right date
        # the index must match with the length of self.input FIX TODO à remplacer
        self.type_error = TypeError("The input canno't be parsed: {}".format(' '.join(self.input)))

    def _declare_translations(self):
        """Translates some attributes"""
        self._oneword_relative = {msg.get('tomorrow',self.lang):self.today + datetime.timedelta(1),
                msg.get('yesterday',self.lang):self.today - datetime.timedelta(1),
                msg.get('week',self.lang): 1, # TODO
                    } # a dict of one word expression relative to today

    def _today(self):
        """Return today"""
        if len(self.input) == 0 or self.input[0] == msg.get('today',self.lang):
            return self.today

    def _oneword(self):
        """Return a date, or a tuple of date
        by passing a word"""
        pass # TODO faire un parser à base de plusieurs mots : next, before, after...

    def _byWords(self):
        """Parse words like next month, etc."""
        units = ['day','week','month','year']
        add = ['next','before','after','previous']
        # on peut rajouter un chiffre avec les units; avec add, on peut ajouter un nom de mois

    def _numbers_without_space(self):
        """manages numbers if len(self.input) == 1
        1-31 -> day of month
        a four characters input: a year
        """
        input = self.input[0]
        return_value=None
        if re.fullmatch(r"[0-3]?[0-9]",input):
            return_value = datetime.date(int(input),self.today.month,self.today.year)
        elif re.fullmatch(r"[0-9]{4}",input):
            return_value = (
                    datetime.date(1,1,int(input)),
                    datetime.date(30,12,int(input)))
        return return_value

    def _todate(self,day=1,month=1,year=today.year) -> datetime.date:
        """wrappers to catch errors"""
        try:
            return datetime.date(int(day),int(month),int(year))
        except (ValueError, TypeError):
            raise self.type_error

    def _dateutil_parser(self) -> datetime.date:
        """wrapper around the dateutil.parser.parse
        Useful to overload this method
        for different locale
        fuzzy is used last"""
        input = ' '.join(self.input)
        try:
            return dateutil.parser.parse(input)
        except ValueError:
            return dateutil.parser.parse(input,fuzzy=True)



    def parse(self) -> TimeSpan:
        """Main method, the only used by user.
        It calls every method to parse the input
        by following the resolution order defined in __init__
        """
        self._declare_translations()
        input_length = len(self.input)
        if input_length > len(self._resolution_order):
            raise self.type_error

        for method in self._resolution_order[input_length]:
            result = method()
            if result:
                return result
        try: 
            return self._dateutil_parser()
        except ValueError:
            raise self.type_error

    def getMonthName(self,number='all') -> str:
        """Get month name in current locale
        if number == 'all', return the list of months"""
        return _getTimeUnitName('month',number)

    def getDayName(self,number='all') -> str:
        """Get weekday name in current locale
        if number == 'all', return the list of days"""
        return _getTimeUnitName('day',number)

    def _getTimeUnitName(self,unit: str, number='all') -> str:
        """Get a time unit name, day or month, in current locale
        if number == 'all', return the list of days"""
        locale = get_locale(self.lang)
        unit_name = {
                'day':calendar.day_name,
                'month':calendar.month_name,
                }[unit]
        with calendar.different_locale(locale) as cdl:
            return unit_name[number] if number != 'all' else unit_name[:]


class EnUsDateParser(_DateParser):
    """Parse us-en english""" # TODO create en-gb
    pass


class FrDateParser(_DateParser):
    """Parse french formatted date"""
    pass        



def dateparser_factory(input: list, lang: str) -> _DateParser:
    """Create a DateParser object following language request"""
    parsers = {
            'fr':FrDateParser,
            'en':EnUsDateParser,
            }
    return parsers[lang](input,lang)

def get_locale(lang: str) -> str:
    """Get locale available in the system"""
    if sys.platform != 'win32':
        locales_availables = subprocess.run(['locale','-a'],stdout=subprocess.PIPE).stdout.decode().split('\n')
        for locale in locales_availables:
            if lang in locale.lower(): # TODO à améliorer s'il faut regarder la localisation en plus
                return locale
        else:
            raise ValueError('The locale requested is not available: {}. Please install it or use your default one'.format(lang))
    else:
        return lang #WONT WORK
      

    
