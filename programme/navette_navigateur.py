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
#        exec(open('manage.py').read())
        subprocess.run(['./manage.py','runserver'])
        
primus = Serveur()

primus.start()
sleep(1)
webbrowser.open_new_tab('localhost:8000/kalendarium/accueil')
print("Local server will be closed within 30 minutes")
primus.join(1800)


