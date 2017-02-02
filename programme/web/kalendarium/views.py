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
    #try:
    if request.GET['type'] == 'jour':
        date, semaine_seule, mois_seul, annee_seule = adjutoria.datevalable(request.GET['date'],'francais')
        debut, fin = adjutoria.AtoZ(semaine_seule,mois_seul,annee_seule,date)

    #retour, err = subprocess.Popen('./theochrone.py', stdout=subprocess.PIPE, shell=True).communicate()
    #titre=retour
    titre = debut
    retour = fin
    return render(request,'kalendarium/accueil.html',locals())
