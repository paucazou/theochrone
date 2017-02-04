#!/usr/bin/python3
# -*-coding:Utf-8 -*
from django import forms
import datetime

class RechercheSimple(forms.Form):
    date_seule = forms.DateField(widget = forms.SelectDateWidget(years=range(1600,4101)),required = True,label="Choisissez une date : ",initial = datetime.date.today) #,attrs={"value":datetime.date.today()})

class RechercheMotClef(forms.Form):
    annees=[]
    for a in range(1600,4101):
        annees.append((a,a))
    annee = forms.IntegerField(widget=forms.Select(choices = annees),max_value=4100,min_value=1600,required=True,initial=datetime.date.today().year)
    recherche = forms.CharField(label="Entrez vos mots-clefs",required=True)
    plus = forms.BooleanField(help_text="Recherche large",required=False)

