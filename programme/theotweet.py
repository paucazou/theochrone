#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module interacts with Tweeter.
It sends tweets to its users about the feast of the day.
It sends tweets to others users to make them discover the theochrone # TODO
It must be used with a crontab to be really useful."""

import annus
import argparse
import datetime
import officia
import phlog
import tweepy
import sys
import time

# arg parser

parser = argparse.ArgumentParser(
            prog='Theotweet',
            formatter_class=argparse.RawTextHelpFormatter,
            description=_("""A script which communicates with Twitter"""),
            epilog=_("Please pray God for me."),
            )

parser.add_argument('auth_file',required=True,type=argparse.FileType('r'),help="Name of the file which contains tokens")
parser.add_argument('-l','--log-level',dest="log_level",type=int,choices=range(-5,5),default=phlog.levels[-1],help="Importance level of the messages that should be printed in the log file")
parse_args.add_argument('-f','--get-followers',dest='get_followers',nargs='*',help="Get the followers of the users screen name entered. Do not enter them with '@' in front of the screen names : @paucazou -> paucazou")

args = parser.parse_args()

# logger
logger = phlog.fileLog(phlog.levels[-1],file_name='_theotweet.log')


lvl = args.log_level
logger.setLevel(lvl)
logger.info("Log level : {}".format(lvl))

# Twitter auth  

accessers = args.auth_file.read().split('\n')
args.auth_file.close()
logger.debug('Authentication file opened')
    
auth = tweepy.OAuthHandler(accessers[0],accessers[1])
auth.set_access_token(accessers[2],accessers[3])
api=tweepy.API(auth)
logger.debug('Auth completed')

# Theochrone stuff
liturgiccal = annus.LiturgicalCalendar('romanus',1962)
language = 'fr'

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
                
def get_screen_names(user,unused_list,used_list):
    """This function gets all the followers of a user (user)
    and add them in unused_list ;
    If a screen name is already present in unused_list or in used_list, does'nt add it.
    Returns a list of new users."""
    for follower in limit_handled(tweepy.Cursor(user.followers).items()):
        follower = follower.screen_name
        if follower not in unused_list and follower not in used_list:
            unused_list.append(follower)
            logger.info('{} added'.format(follower))
    return unused_list
       
def spammer(number):
    """This function sends ads to users already saved in _unused file
    number is the number of users to whom ads will be sent"""
    pass
    
def users_files(data=None,_unused=True,_used=True,read=True):
    """Reads or writes _unused and _used files.
    if read : returns dict with filename as key, and data as value"""
    rw = ('w','r')[read]
    
    
def main():
    """The main function"""
    if args.get_followers:
        logger.info('Loading users files...')
        files = {'_unused':[],'_used':[]}
        for fname in files:
            try:
                with open(fname,'r') as f:
                    files[fname] = f.read().split('\n')
            except FileNotFoundError:
                continue
            
        logger.info('Get followers...')
        for sname in args.get_followers:
            unused_list = get_screen_names(api.get_user(sname),files['_unused'],files['_used']) # rajouter un try, en cas d'erreur
            
        logger.info('Saving unused users file...')
        with open(files['_unused','w') as f:
            f.write('\n'.join(files['_unused']))
    else:
        today = datetime.date.today()
        logger.info("New day : {}".format(today))
        liturgiccal(today.year)
        sendFeastsToUsers(api,today,liturgiccal)
    
if __name__ == '__main__':
    logger.info('App launched')
    main()
    

