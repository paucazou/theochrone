#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
#This module is made to ease logging
# Three modes : console or file or console + file

import logging
import logging.handlers

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
levels = (logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)

def consoleLog(level,logger=logging.getLogger()):
    """Return logger. level is an int which must equal to logging levels."""
    if level not in levels:
        raise ValueError("Unknown level. Level must be CRITICAL : {}, ERROR : {}, WARNING : {}, INFO : {}, DEBUG : {}".format(*levels))
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def fileLog(level,file_name='activity.log',logger=logging.getLogger()):
    if level not in levels:
        raise ValueError("Unknown level. Level must be CRITICAL : {}, ERROR : {}, WARNING : {}, INFO : {}, DEBUG : {}".format(*levels))
    file_handler = logging.handlers.RotatingFileHandler(file_name,'a',1000000,1)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def allLog(level,file_name='activity.log',logger=logging.getLogger()):
    logger = consoleLog(level,logger)
    logger = fileLog(level,file_name,logger)
    return logger
