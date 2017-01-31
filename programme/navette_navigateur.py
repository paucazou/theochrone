#!/usr/bin/python3
# -*-coding:Utf-8 -*
import threading
import os
import sys 
import webbrowser
import subprocess
from time import sleep

### Thread classes ###

class Serveur(threading.Thread):
    """Class which launches local server on port 8000"""

    def run(self):
        """Run by Thread"""
        os.chdir("./web")
        sys.argv = ["manage.py","runserver"]
        #exec(open('./manage.py').read()) # doesn't work for some reason
        subprocess.run(['./manage.py','runserver'])
        
class Navigateur(threading.Thread):
    """Class which opens browser to make Theochrone work on it"""

    def run(self):
        """Run by Thread"""
        sleep(1)
        webbrowser.open_new_tab('localhost:8000/kalendarium/accueil')
        
primus = Serveur()
secundus = Navigateur()

primus.start()
secundus.start()

secundus.join()
primus.join()


