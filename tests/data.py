#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import requests
import dossier
dossier.main()

data = []

def test_url():
    """Tests wether each feast can really contact introibo.fr"""
    for feast in data:
        returned_data = requests.get(feast.link)
        assert returned_data.text == "\n\n\t\t\n        (Il n'y a pas d'article &agrave; cette adresse)\n\n\n"
