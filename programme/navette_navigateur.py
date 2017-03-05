#!/usr/bin/python3
# -*-coding:Utf-8 -*
import http.client
import os
import subprocess
import sys
import threading
import webbrowser

### Thread classes ###

class Serveur(threading.Thread):
    """Class which launches local server on port 8000"""

    def run(self):
        """Run by Thread"""
        chemin = os.path.dirname(os.path.abspath(__file__))
        os.chdir(chemin + "/web") # mettre un abspath
        subprocess.run(['./manage.py','runserver'])
        
### Main ###
primus = Serveur()
primus.start()

taille = len(sys.argv)
adresse = "http://localhost:8000/kalendarium/accueil"
try:
    if taille == 4:
        if sys.argv[1] == "mois":
            adresse = "http://localhost:8000/kalendarium/mois?annee=" + sys.argv[3] + "&mois=" + sys.argv[2]
    if taille == 4:
        adresse = "http://localhost:8000/kalendarium/date_seule?date_seule_day={}&date_seule_month={}&date_seule_year={}".format(sys.argv[1],sys.argv[2],sys.argv[3])
    if taille >= 4:
        if sys.argv[1] == 'inverse':
            adresse = "http://localhost:8000/kalendarium/mot_clef?annee=" + sys.argv[2] + "&recherche="
            for elt in sys.argv[3:]:
                adresse += elt
                if elt != sys.argv[-1]:
                    adresse += '+'
except IndexError:
    adresse = "http://localhost:8000/kalendarium/accueil"

    
local = http.client.HTTPConnection("localhost",port=8000,timeout=1)
local.connection = "off"
while local.connection == "off":
    try:
        local.connect()
        local.connection = "on"
        local.close()
        print("Server is on")
    except ConnectionRefusedError:
        local.connection = "off"
webbrowser.open_new_tab(adresse) # open_new_tab renvoie un bool ; essayer de faire le test avec lui, plutôt qu'avec un connexion http
primus.join() # TODO Faire une commande pour fermer le serveur directement depuis le navigateur


