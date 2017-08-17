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
def translated_messages(file_name,language=args.langue):
    """Return messages translated as a dict
    filename : string : name of the file which requires translation.
    language : string : which language is required. default : args.langue"""
    ### i18n ###
    francais = gettext.translation('messages',loc,languages=['fr'])
    english = gettext.translation('messages',loc,languages=['en'])
    latina = gettext.translation('messages',loc,languages=['la_LA'])

    if language == 'francais':
        francais.install()
    elif language == 'latina':
        latina.install()
    else:
        english.install()


    ### Messages ###
    messages = {}
    messages['theochrone'] = {} # a dict with all the messages used in theochrone.py
    messages['adjutoria'] = {
        _('francais'),
        _('english'),
        _('latina'),
        } # a dict with all the messages used in adjutoria.py
    messages['officia'] = {}
    return messages[file_name]


