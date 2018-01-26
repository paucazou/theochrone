#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
"""A file with arparse and i18n"""
import argparse
import gettext
import os
from command_line import args

loc = os.path.dirname(os.path.abspath(__file__)) + '/i18n'
gettext.install('messages',loc)


args = args()

class MessagesTranslator:
    """This class manages the translation of the messages on the fly"""
    def __init__(self,langs, lang: str):
        """langs is a dict with str as keys matching with a gettext.translation"""
        self.current_lang = lang
        self.langs = langs

    def __get__(self,attribute):
        """Unsafe way to get a translation.
        Uses the current_lang"""
        if '_' + attribute not in self.__dict__:
            raise AttributeError("{} doesn't exist".format(attribute))
        return _(self.__dict__['_' + attribute])

    def __set__(self,attribute,value):
        """Set a value"""
        new_attribute = "_" + attribute
        if new_attribute in self.__dict__:
            raise AttributeError("{} already exists".format(attribute))
        self.__dict__[new_attribute] = value

    def get(message,lang):
        """return a translation of the message in the requested lang"""
        if lang != self.lang:
            self.current_lang = lang
            self.langs[lang].install() # TODO maybe save the translations in a dict when first loaded
        return _(getattr(self,message))

    @staticmethod
    def markToTranslate(value):
        """A static method only used to mark a string litteral
        as translatable.
        You can call it from instance or from class.
        Command-line: xgettext -kmarkToTranslate -j -o OUTPUT INPUT"""
        return value

def translated_messages(file_name,language=args.langue):
    """Return messages translated as a dict
    filename : string : name of the file which requires translation.
    language : string : which language is required. default : args.langue"""
    ### i18n ###
    languages = {
    'fr' : gettext.translation('messages',loc,languages=['fr'])
    'en' : gettext.translation('messages',loc,languages=['en'])
    'la' : gettext.translation('messages',loc,languages=['la_LA'])
    }

    languages[language].install()

    ### Messages ###
    messages = {}
    messages['theochrone'] = MessagesTranslator(langs=languages,lang=language) # a dict with all the messages used in theochrone.py
    messages['adjutoria'] = {
        _('fr'),
        _('en'),
        _('la'),
        } # a dict with all the messages used in adjutoria.py
    messages['officia'] = { # TODO to transfer
            'avent':_('Season of Advent'),
            'nativite':_('Christmastide (Season of Christmas)'),
            'epiphanie':_('Epiphanytide (Season of Christmas)'),
            'apres_epiphanie':_('Season per annum after Epiphany'),
            'septuagesime':_('Season of Septuagesima'),
            'careme':_('Lent (Season of Lent)'),
            'passion':_('Passiontide (Season of Lent)'),
            'paques':_('Eastertide (Season of Easter)'),
            'ascension':_('Ascensiontide (Season of Easter'),
            'octave_pentecote':_('Octave of Pentecost (Season of Easter)'),
            'pentecote':_('Season per annum after Pentecost'),
            }
    return messages[file_name]


