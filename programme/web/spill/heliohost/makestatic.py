#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module calls pages several times in order
to put static files in cache"""

import datetime as d
import phlog
import time
import urllib.request as ur

def main():
    today = d.date.today()
    min = today - d.timedelta(30)
    max = today + d.timedelta(30)
    day = min
    while day <= max:
        while True:
            y,m,dd = day.year, day.month, day.day
            req = ur.Request('http://theochrone.ga/static/shtml/day{}-{}-{}.shtml'.format(y,m,dd),
                    headers={'User-Agent': 'Mozilla/5.0'})
            try:
                page = ur.urlopen(req)
            except HTTPError as error:
                logger.critical(error)
                raise
            if page.headers['CF-Cache-Status'] == 'HIT':
                break
            time.sleep(15)



if __name__ == '__main__':
    main()
