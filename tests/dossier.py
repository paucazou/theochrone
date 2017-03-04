#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module changes directory and makes modules importable"""
def main():
    import os
    import sys
    chemin = os.path.dirname(os.path.abspath(__file__)) + '/../programme/'
    os.chdir(chemin)
    sys.path.append('.')
