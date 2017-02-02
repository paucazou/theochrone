from django.shortcuts import render
import subprocess
import os
import sys

os.chdir('../..')
sys.path.append('.')
import adjutoria
# Create your views here.

def home(request):
    """A function which defines homepage"""
    try:
        if request.GET['type'] == 'jour':
         date, semaine_seule, mois_seul, annee_seule = adjutoria.datevalable([request.GET['date']],'francais',exit=False)
         debut, fin = adjutoria.AtoZ(semaine_seule,mois_seul,annee_seule,date)
    except KeyError:
        date = adjutoria.datevalable([],'francais',exit=False)[0]
    #retour, err = subprocess.Popen('./theochrone.py', stdout=subprocess.PIPE, shell=True).communicate()
    #titre=retour
    titre = request.GET 
    retour = date 
    return render(request,'kalendarium/accueil.html',locals())
