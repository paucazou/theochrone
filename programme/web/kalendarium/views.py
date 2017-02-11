from django.shortcuts import render, redirect
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
         recherche_mot_clef=RechercheMotClef(None),recherche_simple=RechercheSimple(None),mois_entier=MoisEntier(None),mois_seul=False,
         debut=datetime.date.today(),fin=datetime.date.today(),
         mots_clefs='',plus=False,annee=datetime.date.today().year):
    """A function which defines homepage""" 

    with open('./data/samedi.pic','rb') as file:
        pic=pickle.Unpickler(file)
        samedi=pic.load()
    
    retour = ''
    deroule = {}
    if mots_clefs == '':
        Annee = officia.fabrique_an(debut,fin)
        date = debut
        while date <= fin:
            try:
                Annee[date]
            except KeyError:
                Annee[date] = []
            deroule[date] = adjutoria.selection(Annee[date],date,Annee,samedi)
            date = date + datetime.timedelta(1)
        inversion=False
        if mois_seul:
            titre = adjutoria.mois[debut.month - 1]
        else:
            titre = debut
    else:
        titre = mots_clefs
        deroule[titre] = officia.inversons(mots_clefs,adjutoria.datetime.date(annee,1,1),adjutoria.datetime.date(annee,12,31),samedi,exit=False,plus=plus)
        inversion=True

    deroule = sorted(deroule.items())
    locaux = locals() #for development only 

    return render(request,'kalendarium/accueil.html',locals())

def mc_transfert(request):
    recherche_mot_clef = RechercheMotClef(request.GET or None)
    if recherche_mot_clef.is_valid():
        mots_clefs = recherche_mot_clef.cleaned_data['recherche']
        plus = recherche_mot_clef.cleaned_data['plus']
        annee = recherche_mot_clef.cleaned_data['annee']
        return home(request,recherche_mot_clef,mots_clefs=mots_clefs,plus=plus,annee=annee)
    else:
        return home(request, recherche_mot_clef)
        
def date_transfert(request):
    recherche_simple = RechercheSimple(request.GET or None)
    if recherche_simple.is_valid():
        date = recherche_simple.cleaned_data['date_seule']
        return home(request,recherche_simple=recherche_simple,debut=date,fin=date)
    else:
        return home(request,recherche_simple=recherche_simple)

def mois_transfert(request):
    mois_entier = MoisEntier(request.GET or None)
    if mois_entier.is_valid():
        mois = mois_entier.cleaned_data['mois']
        annee = mois_entier.cleaned_data['annee']
        debut = datetime.date(annee,mois,1)
        i=31
        while True:
            try:
                fin = datetime.date(annee,mois,i)
                break
            except ValueError:
                i -= 1
        return home(request,mois_entier=mois_entier,mois_seul=True,debut=debut,fin=fin)
    else:
        return home(request, mois_entier=mois_entier)
    
