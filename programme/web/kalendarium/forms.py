#!/usr/bin/python3
# -*-coding:Utf-8 -*
from django import forms
import datetime

annees=[]
for a in range(1960,2101):
    annees.append((a,a))
    
douze = ('janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre')
propers = {
        'roman':'Romain',
        'american':'Américain',
        'australian':'Australien',
        'brazilian':'Brésilien',
        'canadian':'Canadien',
        'english':'Anglais',
        'french':'Français',
        'new_zealander':'Néo-Zélandais',
        'polish':'Polonais',
        'portuguese':'Portugais',
        'scottish':'Écossais',
        'welsh':'Gallois',
        }

class _BaseResearch(forms.Form):
    """Abstract base class"""
    _empty_value = {'value':''}
    _form_control = {'class':'form-control'}
    pal = forms.BooleanField(widget=forms.HiddenInput(attrs=_empty_value),required=False)
    martyrology = forms.BooleanField(widget=forms.HiddenInput(attrs=_empty_value),required=False)
    proper = forms.CharField(widget=forms.HiddenInput(attrs=_empty_value),required=False)

class SharedResearch(forms.Form):
    """Used by all the research forms"""
    pal = forms.BooleanField(label="Inclure les messes Pro Aliquibus Locis",required=False)
    martyrology = forms.BooleanField(label="Dans le Martyrologe Romain",required=False)
    proper = forms.CharField(widget=forms.Select(choices=sorted(propers.items()),
        attrs={'class':'form-control'}),
        required=False,label="Choisissez le propre",initial='roman')

class RechercheSimple(_BaseResearch):
    """A class which defines a form for a research by an only date"""
    date_seule = forms.DateField(widget = forms.SelectDateWidget(years=range(1960,2100),
                                 attrs = {
                                     'class' : "form-control"}),
                                 required = True,label="Choisissez une date",initial = datetime.date.today
                                 )

class RechercheMotClef(_BaseResearch):
    """A class which defines a form for a research by key words"""
    annee = forms.IntegerField(widget=forms.Select(choices = annees,attrs = _BaseResearch._form_control),
                                     max_value=2100,min_value=1960,
                               required=True,initial=datetime.date.today().year)
    recherche = forms.CharField(widget=forms.TextInput(attrs=_BaseResearch._form_control),
        label="Entrez vos mots-clefs",required=True)
    plus = forms.BooleanField(label="Recherche large",required=False)

class MoisEntier(_BaseResearch):
    """A class which defines a form for a reserch of a complete month"""
    annee = forms.IntegerField(widget=forms.Select(choices = annees,attrs = {
                                     'class' : "form-control"}),max_value=2100,min_value=1960,
                               required=True,initial=datetime.date.today().year)
    mois = forms.IntegerField(widget = forms.Select(choices = [(i+1,month.capitalize()) for i,month in enumerate(douze)],attrs =_BaseResearch._form_control),
                              max_value=12,min_value=1,required = True,
                              initial = datetime.date.today().month)
    
    
class ContactForm(forms.Form):
    """A class which defines a contact form"""
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
