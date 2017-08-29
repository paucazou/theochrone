#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
from django import forms

class Dispatch(forms.Form):
    """This class checks the get args to use appropriate view
    with AJAX"""
    pages_available = ('day','test')
    page = forms.ChoiceField(required=True,choices=[(item,item) for item in pages_available])

class Info(forms.Form):
    """Class used to collect data with AJAX"""
    urlinfo = forms.CharField(required=True)
