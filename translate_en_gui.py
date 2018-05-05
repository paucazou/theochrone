#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module translates the english
strings of the GUI"""

import xml.etree.ElementTree as ET

file_path = "./programme/gui/i18n/theochrone.en.ts" # it supposes that you call this file from this folder
tree = ET.parse(file_path)
root = tree.getroot()

for context in root:
    for child in context:
        if child.tag == 'message':
            message = child
            # the translation is equal to the original source
            message[2].text = message[1].text 
            message[2].attrib = {} # remove type=unfinished

tree.write(file_path)
