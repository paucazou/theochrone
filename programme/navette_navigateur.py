#!/usr/bin/python3
# -*-coding:Utf-8 -*
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
        os.chdir("./web")
        sys.argv = ["manage.py","runserver"]
#        exec(open('manage.py').read())
        subprocess.run(['./manage.py','runserver'])
        
### Main ###
primus = Serveur()
primus.start()

return_code = 1
while return_code != 0:
    """Waits until the server is on. 'nc' tries to connect to server at '8000' port. Works on *nix."""
    return_code = subprocess.call(['nc','-vz','localhost','8000'])
    
webbrowser.open_new_tab('localhost:8000/kalendarium/accueil')
print("Local server will be closed within 30 minutes")
primus.join(1800)


