#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the State object,
which represents the state of the central
widget of the main window"""

class State:
    """State of the central widget in a
    main window"""
    def __call__(self,**kwargs):
        """Called when state changes.
        kwargs become the attributes of the
        instance. They depend on the type of the
        central widget.
        required keys are type and data, as they
        allow the object to determine the others keys.
        No verification is made."""
        self.__dict__ = kwargs

    def next(self):
        """Changes the instance to the next item,
        if possible."""
        pass

    def previous(self):
        """Changes the instance to the previous item,
        if possible"""
        pass
