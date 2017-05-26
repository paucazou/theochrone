#!/usr/bin/python3
# -*-coding:Utf-8 -*
from django import forms
import datetime

annees=[]
for a in range(1960,2101):
    annees.append((a,a))
    
douze = ('janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre')

class RechercheSimple(forms.Form):
    """A class which defines a form for a research by an only date"""
    date_seule = forms.DateField(widget = forms.SelectDateWidget(years=range(1960,2100),
                                 attrs = {
                                     'class' : "form-control"}),
                                 required = True,label="Choisissez une date",initial = datetime.date.today
                                 )

class RechercheMotClef(forms.Form):
    """A class which defines a form for a research by key words"""
    annee = forms.IntegerField(widget=forms.Select(choices = annees,attrs = {
                                     'class' : "form-control"}), max_value=2100,min_value=1960,
                               required=True,initial=datetime.date.today().year)
    recherche = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'},),
        label="Entrez vos mots-clefs",required=True)
    plus = forms.BooleanField(label="Recherche large",required=False)

class MoisEntier(forms.Form):
    """A class which defines a form for a reserch of a complete month"""
    annee = forms.IntegerField(widget=forms.Select(choices = annees,attrs = {
                                     'class' : "form-control"}),max_value=2100,min_value=1960,
                               required=True,initial=datetime.date.today().year)
    mois = forms.IntegerField(widget = forms.Select(choices = [(i+1,month.capitalize()) for i,month in enumerate(douze)],attrs = {
                                     'class' : "form-control"}),
                              max_value=12,min_value=1,required = True,
                              initial = datetime.date.today().month)
    
class ContactForm(forms.Form):
    """A class which defines a contact form"""
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
