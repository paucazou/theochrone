from django.shortcuts import render
import subprocess
import os
import sys
import pickle
from .forms import Recherche

#os.chdir('../..')
os.chdir("/home/partage/.scripts/projet_liturgie/wip_fetes/programme")
sys.path.append('.')
import adjutoria
import officia
# Create your views here.

def home(request):
    """A function which defines homepage"""
    form = Recherche(request.GET or None)
    if form.is_valid():
        date = form.cleaned_data['date_seule']
    else:
        date = adjutoria.datetime.date.today() 
    Annee = officia.fabrique_an(date,date)
    with open('./data/samedi.pic','rb') as file:
        pic=pickle.Unpickler(file)
        samedi=pic.load()
    try:
        Annee[date]
    except KeyError:
        Annee[date] = []
    celebrations = adjutoria.selection(Annee[date],date,Annee,samedi)
    retour = ''
    for a in celebrations:
        retour += a.nom['francais'] + '<br />'

    return render(request,'kalendarium/accueil.html',locals())
