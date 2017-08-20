#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the whole program, as it is intented to be distributed to final users."""

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))



def main():
    """Launch the main function.
    This function is intended to work for windows standalone only.
    If you want this function to work, please rename theochrone.pyw -> theochrone.py"""
    import theochrone
    theochrone.main()
