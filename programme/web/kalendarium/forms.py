#!/usr/bin/python3
# -*-coding:Utf-8 -*
from django import forms
import datetime

class Recherche(forms.Form):
    date_seule = forms.DateField(widget = forms.SelectDateWidget(years=range(1600,4101)),required = True,label="Choisissez une date : ",initial = datetime.date.today) #,attrs={"value":datetime.date.today()})

