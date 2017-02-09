from django.shortcuts import render, redirect
import subprocess
import os
import sys
import pickle
from .forms import * 

chemin = os.path.dirname(os.path.abspath(__file__)) + '/../..'
os.chdir(chemin)
sys.path.append('.')
import adjutoria
import officia
# Create your views here.

def home(request,
         recherche_mot_clef=RechercheMotClef(None),recherche_simple=RechercheSimple(None),date=datetime.date.today(),
         mots_clefs='',plus=False,annee=datetime.date.today().year):
    """A function which defines homepage"""
    """if recherche_simple.is_valid():
        date = recherche_simple.cleaned_data['date_seule']
    if recherche_mot_clef.is_valid():
        mots_clefs = recherche_mot_clef.cleaned_data['recherche']
        plus = recherche_mot_clef.cleaned_data['plus']
        try:
            annee = recherche_mot_clef.cleaned_data['annee']
        except TypeError:
            annee = adjutoria.datetime.date.today().year""" 

    with open('./data/samedi.pic','rb') as file:
        pic=pickle.Unpickler(file)
        samedi=pic.load()
    
    retour = ''
    if mots_clefs == '':
        Annee = officia.fabrique_an(date,date)
        try:
            Annee[date]
        except KeyError:
            Annee[date] = []
        liste = adjutoria.selection(Annee[date],date,Annee,samedi)
        titre=date
        inversion=False
    else:
        liste = officia.inversons(mots_clefs,adjutoria.datetime.date(annee,1,1),adjutoria.datetime.date(annee,12,31),samedi,exit=False,plus=plus)
        titre = mots_clefs
        inversion=True

    locaux = locals() #for development alone 

    return render(request,'kalendarium/accueil.html',locals())

def mc_transfert(request):
    recherche_mot_clef = RechercheMotClef(request.GET or None)
    if recherche_mot_clef.is_valid():
        mots_clefs = recherche_mot_clef.cleaned_data['recherche']
        plus = recherche_mot_clef.cleaned_data['plus']
        annee = recherche_mot_clef.cleaned_data['annee']
    return home(request,recherche_mot_clef,mots_clefs=mots_clefs,plus=plus,annee=annee)
        
def date_transfert(request):
    recherche_simple = RechercheSimple(request.GET or None)
    if recherche_simple.is_valid():
        date = recherche_simple.cleaned_data['date_seule']
    return home(request,recherche_simple=recherche_simple,date=date)

def mois_transfert(request):
    mois_seul = MoisSeul(request.GET or None)
    if mois_seul.is_valid():
        debut = mois_seul.cleaned_data['debut']
        fin = mois_seul.cleaned_data['fin']
    return home(request,mois_seul=mois_seul,debut=debut,fin=fin)
    
