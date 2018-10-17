#!/usr/bin/python3
# -*-coding:Utf-8 -*
from django import forms
import datetime

annees=[(y,y) for y in range(1960,2101)]
    
douze = ('janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre')
propers = {
        'roman':'Romain',
        'american':'Américain',
        'australian':'Australien',
        'brazilian':'Brésilien',
        'canadian':'Canadien',
        'english':'Anglais',
        'french':'Français',
        'newzealander':'Néo-Zélandais',
        'polish':'Polonais',
        'portuguese':'Portugais',
        'scottish':'Écossais',
        'welsh':'Gallois',
        'strasburger':'Strasbourgeois',
        }
# forms shared

palForm = forms.BooleanField(label="Inclure les messes Pro Aliquibus Locis",required=False)
properForm = forms.CharField(widget=forms.Select(choices=sorted(propers.items()),
    attrs={'class':'form-control'}),
    required=False,label="Choisissez le propre",initial='roman')
# widget attributes

_form_control = {'class':'form-control'}

class _BaseResearch(forms.Form):
    """Abstract base class"""
    _empty_value = {'value':''}
    pal = forms.BooleanField(widget=forms.HiddenInput(attrs=_empty_value),required=False)
    martyrology = forms.BooleanField(widget=forms.HiddenInput(attrs=_empty_value),required=False)
    proper = forms.CharField(widget=forms.HiddenInput(attrs=_empty_value),required=False)

class SharedResearch(forms.Form):
    """Used by all the research forms"""
    pal = palForm
    martyrology = forms.BooleanField(label="Dans le Martyrologe Romain",required=False)
    proper = properForm
    field_order = ['martyrology','pal','proper']

class RechercheSimple(_BaseResearch):
    """A class which defines a form for a research by an only date"""
    date_seule = forms.DateField(widget = forms.SelectDateWidget(years=range(1960,2100),
                                 attrs = {
                                     'class' : "form-control"}),
                                 required = True,label="Choisissez une date",initial = datetime.date.today
                                 )

class RechercheMotClef(_BaseResearch):
    """A class which defines a form for a research by key words"""
    annee = forms.IntegerField(widget=forms.Select(choices = annees,attrs = _form_control),
                                     max_value=2100,min_value=1960,
                               required=True,initial=datetime.date.today().year)
    recherche = forms.CharField(widget=forms.TextInput(attrs=_form_control),
        label="Entrez vos mots-clefs",required=True)
    plus = forms.BooleanField(label="Recherche large",required=False)

class MoisEntier(_BaseResearch):
    """A class which defines a form for a reserch of a complete month"""
    annee = forms.IntegerField(widget=forms.Select(choices = annees,attrs = {
                                     'class' : "form-control"}),max_value=2100,min_value=1960,
                               required=True,initial=datetime.date.today().year)
    mois = forms.IntegerField(widget = forms.Select(choices = [(i+1,month.capitalize()) for i,month in enumerate(douze)],attrs =_form_control),
                              max_value=12,min_value=1,required = True,
                              initial = datetime.date.today().month)
    
    
class ContactForm(forms.Form):
    """A class which defines a contact form"""
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()

class ExportResults(forms.Form):
    """A class which defines a form to export
    results of the Theochrone for a whole year"""
    # variables used below to define real items of the form
    _current_year = datetime.date.today().year
    _start = _current_year - 5
    _end = _current_year + 5
    # year to export
    year = forms.IntegerField(widget=forms.Select(
        choices = [(y,y) for y in range(_start,_end+1)],attrs=_form_control),
        max_value=_end,min_value=_start,
        required = True, initial = _current_year,
        label="Choisissez l'année à exporter")
    # format of the file returned
    format = forms.ChoiceField(widget=forms.RadioSelect,choices=(('ics','ICS'),('csv','CSV')),
            required = True,label="Choisissez le format de votre fichier",initial='ics')
    # proper
    proper = properForm
    #pal
    pal = palForm
    field_order = ['format','year','proper','pal']

class OptionsWidgetDay(forms.Form):
    """Defines the options that can be used to create a widget"""
    proper = properForm
    pal=palForm

class OptionsWidgetDayMobile(forms.Form):
    """Defines the options that can be used to create the mobile widget"""
    proper = properForm
