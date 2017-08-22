#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module interacts with Tweeter.
It sends tweets to its users about the feast of the day.
It sends tweets to others users to make them discover the theochrone # TODO
It must be used with a crontab to be really useful."""

import annus
import datetime
import officia
import phlog
import tweepy
import sys
import time

# logger
logger = phlog.fileLog(phlog.levels[-1],file_name='_theotweet.log')

try:
    lvl = phlog.levels[int(sys.argv[2])]
    logger.setLevel(lvl)
    logger.info("Log level : {}".format(lvl))
except (IndexError, ValueError) as error:
    logger.setLevel(phlog.levels[1])

# Twitter auth
if len(sys.argv) == 1:
    logger.critical('File not specified')
    sys.exit('File not specified')
    
with open(sys.argv[1]) as file:
    accessers = file.read().split('\n')
logger.debug('Authentication file opened')
    
auth = tweepy.OAuthHandler(accessers[0],accessers[1])
auth.set_access_token(accessers[2],accessers[3])
api=tweepy.API(auth)
logger.debug('Auth done')
api.me()

# Theochrone stuff
liturgiccal = annus.LiturgicalCalendar('romanus',1962)
language = 'francais'
oldtoday=datetime.date.today() - datetime.timedelta(1)

logger.debug('Theochrone loaded')

def limit_handled(cursor):
    """This function limits the access to the api
    if twitter raises rate limit error"""
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            logger.warning('RateLimitError')
            time.sleep(2 * 60)

def sendFeastsToUsers(api,today,liturgiccal):
    """This function sends each day tweets to users with the name of the feast."""
    msg = officia.affichage(liste=liturgiccal[today],
                            langue=language,
                            date=today,
                            split=True,
                            date_affichee=True,
                            temps_liturgique=False,
                            degre=False,
                            temporal_ou_sanctoral=False,
                            couleur=False,
                            transfert=False,
                            station=False,
                            recherche=False,
                            jour_semaine=False,
                            verbose=False,)
    for follower in limit_handled(tweepy.Cursor(api.followers).items()):
        update_status([follower.screen_name],msg)

def update_status(users=[],texts=[]):
    """Update status. Specifies a list of users to send the text to.
    If status is greater than 140 chars, divides tweet in as many parts as necessary.
    This is a recursive function."""
    maxnb = 140
    allusers = ' '.join(
                ["@{}".format(user) for user in users])
    for txt in texts:
        msg = "{} {}".format(allusers, txt)
        
        if len(msg) <= maxnb:
            logger.debug("Msg sent in less than 141 char : {}".format(msg))
            api.update_status(msg)
        elif len(allusers) == maxnb / 2:
            for user in users:
                logger.warning('Too many users : recursive used')
                update_status([user],texts)
            continue
        else:
            logger.warning("Msg must be split : {}".format(msg))
            split_msg = msg.split()
            new_msg = ''
            new_msgs = []
            i = 1
            for word in split_msg:
                copy_msg = "{} {}".format(new_msg,word)
                if len(copy_msg) > maxnb - 4:
                    new_msgs.append(new_msg + " {}/".format(i))
                    i+=1
                    new_msg = word
            
            for msg in new_msgs:
                logger.debug('Msg splitted : {}'.format(msg))
                api.update_status(msg+i) # retenter plus tard en cas d'erreur
        
def main():
    """The main function"""
    today = datetime.date.today()
    logger.info("New day : {}".format(today))
    liturgiccal(today.year)
    sendFeastsToUsers(api,today,liturgiccal)
    
if __name__ == '__main__':
    logger.info('App launched')
    main()
    

