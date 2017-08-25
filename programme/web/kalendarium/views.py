from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
import os
import sys
from .forms import * 


# Create your views here.

chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/../..')
sys.path.append(programme)
import annus
import adjutoria
import officia

Annee = annus.LiturgicalCalendar()
    
def home(request,
         recherche_mot_clef=RechercheMotClef(None),recherche_simple=RechercheSimple(None),mois_entier=MoisEntier(None),mois_seul=False,
         debut=datetime.date.today(),fin=datetime.date.today(),
         mots_clefs='',plus=False,annee=datetime.date.today().year,
         contact_success=False):
    """A function which defines homepage. It is also used
    by other pages to print common code.
    It takes many arguments :
    - a request sent by client ;
    - three GET forms whith None as default value  : recherche_mot_clef, recherche_simple, mois_entier ;
    - mois_seul : a bool to define whether a complete month will be returned or not ;
    - debut : a datetime.date for the older date ;
    - fin : a datetime.date for the latest date ;
    - mots_clefs : a string used for research ;
    - plus : a bool used to know whether the research must be large, or not ;
    - annee : the year ;
    """
    trunk = 'https://theochrone.000webhostapp.com/static/downloads/'
    downloads = {'windows32':trunk + 'windows/theochrone32.zip',
                 'windows64':trunk + 'windows/theochrone64.zip',
                 'linux32':trunk + 'linux/theochrone32',
                 'linux64':trunk + 'linux/theochrone64',
                 'osx32':trunk + 'osx/theochrone32',
                 'osx64':trunk + 'osx/theochrone64',
                 'python':trunk + 'python/Theochrone.zip',
                 } # list of downloads
    
    retour = ''
    deroule = {}
    if mots_clefs == '':        
        date = debut
        Annee(date.year)
        while date <= fin:
            deroule[date] = Annee[date]
            date = date + datetime.timedelta(1)
        inversion=False
        if mois_seul:
            titre = officia.mois[debut.month - 1]
        else:
            titre = debut
    else:
        titre = mots_clefs
        Annee(annee)
        deroule[titre] = officia.inversons(mots_clefs,Annee,datetime.date(annee,1,1),datetime.date(annee,12,31),langue='francais',exit=False,plus=plus)
        inversion=True

    for value in deroule.values():
        for elt in value:
            elt.temps_liturgique_ = "T" + officia.affiche_temps_liturgique(elt,langue='francais')[1:]
    deroule = sorted(deroule.items())

    return render(request,'kalendarium/accueil.html',locals())

def mc_transfert(request):
    """A function which takes the request argument (GET) and returns the home function with the results of a research by name"""
    recherche_mot_clef = RechercheMotClef(request.GET or None)
    if recherche_mot_clef.is_valid():
        mots_clefs = recherche_mot_clef.cleaned_data['recherche']
        plus = recherche_mot_clef.cleaned_data['plus']
        annee = recherche_mot_clef.cleaned_data['annee']
        return home(request,recherche_mot_clef,mots_clefs=mots_clefs,plus=plus,annee=annee)
    else:
        return home(request, recherche_mot_clef)
        
def date_transfert(request):
    """A function which takes the request arguments (GET) and returns the home function with the results of a research by date"""
    recherche_simple = RechercheSimple(request.GET or None)
    if recherche_simple.is_valid():
        date = recherche_simple.cleaned_data['date_seule']
        return home(request,recherche_simple=recherche_simple,debut=date,fin=date)
    else:
        return home(request,recherche_simple=recherche_simple)

def mois_transfert(request):
    """A function which takes the request arguments (GET) and returns the home function with the results of a research of a complete month"""
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
    
def contact(request):
    """A function which takes the request arguments (POST) and returns the home function with success"""
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            mail_list = ['paucazou@yahoo.fr',from_email]
            try:
                send_mail(subject, message, from_email, ['paucazou@yahoo.fr'])
                send_mail(subject, message, from_email, [from_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return home(request, contact_success = True)
    return home(request, contact_success = False)


