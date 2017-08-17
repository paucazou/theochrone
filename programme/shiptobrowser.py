#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import http.client
import phlog
import os
import sys
import threading
import webbrowser

logger = phlog.loggers['console']

### Thread classes ###

class Server(threading.Thread):
    """Class which launches local server on port 8000"""

    def run(self):
        """Run by Thread"""
        path=os.path.dirname(os.path.abspath(__file__))+'/web'
        os.chdir(path)# change dir to use django manage
        sys.path.append(path)
        import manage
        logger.info(sys.path)
        sys.argv = ['./manage.py','runserver']
        logger.info(sys.argv)
        manage.manager()
   
### Functions ###

def openBrowser(search_type=None,date=None,keywords=None):
    """Waits until server is on.
    Opens browser and request for corresponding values"""
    primus = Server()
    primus.start()

    link = "http://localhost:8000/kalendarium/accueil"
    if search_type == 'month':
        link = "http://localhost:8000/kalendarium/mois?annee={}&mois={}#resultup".format(date.year,date.month)
    elif search_type == 'day':
        link = "http://localhost:8000/kalendarium/date_seule?date_seule_day={}&date_seule_month={}&date_seule_year={}#resultup".format(date.day,date.month,date.year)
    elif search_type == 'reverse':
        logger.info(keywords)
        link = "http://localhost:8000/kalendarium/mot_clef?annee={}&recherche={}#resultup".format(date.year,'+'.join(keywords))
    
    local = http.client.HTTPConnection("localhost",port=8000,timeout=1)
    local.connection = "off"
    while local.connection == "off":
        try:
            local.connect()
            local.connection = "on"
            local.close()
            logger.info("Server is on")
        except ConnectionRefusedError:
            local.connection = "off"
    webbrowser.open_new_tab(link) # open_new_tab renvoie un bool ; essayer de faire le test avec lui, plutôt qu'avec un connexion http
    primus.join()

if __name__ == '__main__':
    openBrowser()
