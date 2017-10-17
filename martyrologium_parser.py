#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module was made to parse 12
html files and return entries for each day
of the martyrology.
With little modifications, it could be use for other purposes"""

import html.parser
import programme.phlog as phlog
import re
import urllib.request as request

logger = phlog.loggers['console']

months = (None,'JANUARIUS', ) # tuple of months in latin
class MartyrologiumParser(html.parser.HTMLParser):
    def __init__(self):
        self.start = False # if True, start returning text
        self.current_date = [0,0] # [month,day] : int
        self.texts = [''] # a list of the texts for each day
        html.parser.HTMLParser.__init__(self)

    def handle_endtag(self,tag):
        """Checks if it should start to return data"""
        if not self.start:
            if tag == 'table':
                self.start = True
                self.current_date[1] += 1
                self.texts.append('')

    def handle_starttag(self,tag,attrs):
        """Checks if it shouls stop to return data"""
        if self.start:
            if tag == 'table':
                self.start = False

    def handle_data(self,data):
        if self.start:
            self.texts[self.current_date[1]] += data
        if data in months:
            self.current_date[0] = months.index(data)
            logger.info(self.current_date)
        if 'Deo gratias' in data:
            self.start = False

    def format_data(self):
        """Format data returned : deletes useless entries, deletes useless \\n"""
        self.texts = self.texts[1:12]
        self.texts = [ re.sub(r"([^.])(\xa0|\n)",r'\1',elt) for elt in self.texts ]


