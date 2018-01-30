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

class MessagesTranslator: # TEST
    """This class manages the translation of the messages on the fly.
    Please do not include strings related to the content of the Fete objects themselves"""
    def __init__(self,langs, lang: str): # TEST
        """langs is a dict with str as keys matching with a gettext.translation"""
        self.current_lang = lang
        self.langs = langs

    def __getattr__(self,attribute: str): # TEST
        """Unsafe way to get a translation.
        Uses the current_lang"""
        real_attribute = '_' + attribute
        if real_attribute not in self.__dict__:
            raise AttributeError("{} doesn't exist".format(attribute))
        return _(self.__dict__[real_attribute]) if real_attribute not in ('_current_lang','_langs') else self.__dict__[real_attribute]

    def __setattr__(self,attribute: str,value: str): # TEST
        """Set a value"""
        if attribute.startswith('_'):
            raise AttributeError("Please do not set attributes starting with `_`: {}".format(attribute))
        new_attribute = "_" + attribute
        if new_attribute in self.__dict__ and new_attribute not in ('_current_lang','_langs'):
            raise AttributeError("{} already exists".format(attribute))
        self.__dict__[new_attribute] = value

    def get(self,message: str,lang: str): # TEST
        """return a translation of the message in the requested lang"""
        self.setLang(lang)
        return _(getattr(self,message))

    def markToTranslate(self,value: str,attribute: str) -> str: # TEST
        """Mark a string literal to be translated
        and save it into the object under the attribute name
        `example = MessagesTranslator(langs,lang)
        example.markToTranslate("Praise the Lord, o my heart",'praise')
        print(example.praise) # print Praise the Lord, o my heart`
        Command-line: xgettext -kmarkToTranslate -j -o OUTPUT INPUT"""
        self.__setattr__(attribute,value)
        return value

    def setLang(self,lang: str): # TEST
        """Install 'lang' translation"""
        if lang != self.current_lang:
            self.current_lang = ('en',lang)[lang in self.langs]
            self.langs.get(lang,self.langs['en']).install() # TODO maybe save the translations in a dict when first loaded


def translated_messages(file_name,language=args.langue):
    """Return messages translated as a dict
    filename : string : name of the file which requires translation.
    language : string : which language is required. default : args.langue"""
    ### i18n ###
    languages = {
    'fr' : gettext.translation('messages',loc,languages=['fr']),
    'en' : gettext.translation('messages',loc,languages=['en']),
    'la' : gettext.translation('messages',loc,languages=['la_LA']),
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
    messages['officia'] = { 
            }
    dateparse_msg = MessagesTranslator(langs=languages,lang=language)
    dateparse_msg.markToTranslate('today','today')

    messages['dateparse'] = dateparse_msg
    
    return messages[file_name]

