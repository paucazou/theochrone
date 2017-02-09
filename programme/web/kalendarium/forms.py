#!/usr/bin/python3
# -*-coding:Utf-8 -*
from django import forms
import datetime

annees=[]
for a in range(1960,2101):
    annees.append((a,a))
    
douze = [(1,'janvier'),(2,'février'),(3,'mars'),(4,'avril'),('mai',5),('juin',6),('juillet',7),('août',8),('septembre',9),('octobre',10),(11,'novembre'),('décembre',12)]

class RechercheSimple(forms.Form):
    date_seule = forms.DateField(widget = forms.SelectDateWidget(years=range(1960,2100)),required = True,label="Choisissez une date : ",initial = datetime.date.today) #,attrs={"value":datetime.date.today()})

class RechercheMotClef(forms.Form):
    annee = forms.IntegerField(widget=forms.Select(choices = annees),max_value=2100,min_value=1960,required=True,initial=datetime.date.today().year)
    recherche = forms.CharField(label="Entrez vos mots-clefs",required=True)
    plus = forms.BooleanField(help_text="Recherche large",required=False)

class MoisEntier(forms.Form):
    annee = forms.IntegerField(widget=forms.Select(choices = annees),max_value=2100,min_value=1960,required=True,initial=datetime.date.today().year)
    mois = forms.CharField(widget = forms.Select(choices = douze),required = True,initial = douze[datetime.date.today().month - 1])
