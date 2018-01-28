#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module defines classes 
which take a list of strings and return a date object"""
import calendar
import datetime

class _DateParser:
    """Abstract base class"""
    def __init__(self,input: list,lang: str):
        """Defines attributes"""
        self.input = input
        self.lang = lang
        self.today = datetime.date.today()
        self._resolution_order = [
                (self._today,),

                ] # a list of lists with the methods in the good order to return the right date
        # the index must match with the length of self.input

    def _today(self):
        """Return today"""
        if len(self.input) == 0:
            return self.today

    def parse(self) -> datetime.date:
        """Main method, the only used by user.
        It calls every method to parse the input
        by following the resolution order defined in __init__
        """
        type_error = TypeError("The input canno't be parsed: {}".format(' '.join(self.input)))
        input_length = len(self.input)
        if input_length > len(self._resolution_order):
            raise type_error

        for method in self._resolution_order[input_length]:
            result = method()
            if result:
                return result
        raise type_error


class EnUsDateParser(_DateParser):
    """Parse us-en english""" # TODO create en-uk
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
    
