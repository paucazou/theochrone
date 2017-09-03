#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
# This module is intented to create a virgin database with sqlite3
# Rules :
# Each class a different table
# Only numbers (integers and reals (float) are directly stored in the instance 
# texts, lists, dicts, etc. are stored as integers which points to another table,
# whose name is equal to the key : ex : 'station' key points to 'station' table.
# Lists are represented by a text value with this separator : @@@
# dicts should be reprenseted by an integer pointing to another table
# As much as possible, the database should be absolutely automated.
# The user is supposed to give an instance, and the database store it automatically,
# even if the class is not previously set, and even if the class does not yet contains new attributes.
# It should be also possible to turn away some attributes which are only useful when data are loaded,
# for instance 'date'. A list of some of these attributes should be set somewhere, probably in the class definition
