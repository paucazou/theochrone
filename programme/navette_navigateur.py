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
    
webbrowser.open_new_tab('http://localhost:8000/kalendarium/accueil') # open_new_tab renvoie un bool ; essayer de faire le test avec lui, plutôt qu'avec un connexion http
print("Local server will be closed within 30 minutes") # doesn't work
primus.join(1.0)


