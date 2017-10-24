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
import martyrology
import officia

martyrology_instance = martyrology.Martyrology()
Annee = annus.LiturgicalCalendar()
host = "localhost:8000"
s=''
    
# use online

def home(request,
         recherche_mot_clef=RechercheMotClef(None),recherche_simple=RechercheSimple(None),mois_entier=MoisEntier(None),mois_seul=False,
         debut=datetime.date.today(),fin=datetime.date.today(),
         mots_clefs='',plus=False,annee=datetime.date.today().year):
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
    retour = ''
    deroule = {}
    if mots_clefs == '':
        hashtag = 'resultup'
        if debut == fin: #à mettre dans le template
            next_item = officia.datetime_to_link(fin + datetime.timedelta(1),host,hashtag=hashtag,s=s)
            previous_item = officia.datetime_to_link(debut - datetime.timedelta(1),host,hashtag=hashtag,s=s)
        else:
            next_item = officia.month_to_link(fin,host,1,hashtag,s)
            previous_item = officia.month_to_link(debut,host,-1,hashtag,s)
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
        deroule[titre] = officia.inversons(mots_clefs,Annee,datetime.date(annee,1,1),datetime.date(annee,12,31),langue='fr',exit=False,plus=plus)
        inversion=True

    for value in deroule.values():
        for elt in value:
            elt.temps_liturgique_ = "T" + officia.affiche_temps_liturgique(elt,langue='fr')[1:]
    deroule = sorted(deroule.items())

    return render(request,'kalendarium/accueil.html',locals())

def mc_transfert(request):
    """A function which takes the request argument (GET) and returns the home function with the results of a research by name"""
    recherche_mot_clef = RechercheMotClef(request.GET or None)
    if recherche_mot_clef.is_valid():
        if recherche_mot_clef.cleaned_data['martyrology']:
            result = martyrology_kw(request,recherche_mot_clef)
        else:
            mots_clefs = recherche_mot_clef.cleaned_data['recherche']
            plus = recherche_mot_clef.cleaned_data['plus']
            annee = recherche_mot_clef.cleaned_data['annee']
            result = home(request,recherche_mot_clef,mots_clefs=mots_clefs,plus=plus,annee=annee)
    else:
        result = home(request, recherche_mot_clef)
    return result
        
def date_transfert(request):
    """A function which takes the request arguments (GET) and returns the home function with the results of a research by date"""
    recherche_simple = RechercheSimple(request.GET or None)
    if recherche_simple.is_valid():
        date = recherche_simple.cleaned_data['date_seule']
        if recherche_simple.cleaned_data['martyrology']:
            result = martyrology_date(request,date,recherche_simple)
        else:
            result = home(request,recherche_simple=recherche_simple,debut=date,fin=date)
    else:
        result = home(request,recherche_simple=recherche_simple)
    return result

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
    
def martyrology_date(request,date=None,recherche_simple=None):
    """Return martyrology for a date"""
    if not date:
        return home(request)
    result = (martyrology_instance.daytext(date,'fr'),) # a tuple in order to iterate in template
    martyrology = True
    recherche_mot_clef=RechercheMotClef(None)
    mois_entier=MoisEntier(None)
    hashtag = 'resultup'
    next_item = officia.datetime_to_link(date + datetime.timedelta(1),host,'on',hashtag,s)
    previous_item = officia.datetime_to_link(date - datetime.timedelta(1),host,'on',hashtag,s)
    main_title = martyrology_instance.name['fr']
    credits = martyrology_instance.credits('fr')
    titre = "Martyrologe romain : {}".format(result[0].title)
    return render(request,'kalendarium/accueil.html',locals())

def martyrology_kw(request,recherche_mot_clef=None):
    """Return martyrology for a keyword reseach"""
    inversion = martyrology = True
    keywords = recherche_mot_clef.cleaned_data['recherche']
    max_nb_returned = [10,5][not recherche_mot_clef.cleaned_data['plus']]
    result = martyrology_instance.kw(keywords.split(),'fr',max_nb_returned=max_nb_returned,year=recherche_mot_clef.cleaned_data['annee'])
    mois_entier=MoisEntier(None)
    recherche_simple=RechercheSimple(None)
    hashtag = 'resultup'
    credits = martyrology_instance.credits('fr')
    titre = "Martyrologe romain : {}".format(keywords)
    return render(request,'kalendarium/accueil.html',locals())
    
# contact
def contact(request):
    """A function which takes the request arguments (POST)
    and returns the view with success"""
    contact_success = False
    titre = "Contact"
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = '[Theochrone] ' + form.cleaned_data['subject']
            from_email = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            mail_list = ['paucazou@yahoo.fr',from_email]
            try:
                send_mail(subject, message, from_email, ['paucazou@yahoo.fr'])
                send_mail(subject, message, from_email, [from_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            contact_success = True
    return render(request,'kalendarium/contact.html',locals())

def contribute(request):
    """Contribute and who are we view"""
    title = "Contribuer" # TODO changer le titre en fonction de l'endroit dans la page
    return render(request,'kalendarium/contribute.html',locals())

# get Theochrone
def widget(request):
    """View for widget page"""
    title = "Installer le widget sur votre site"
    fpath = os.path.abspath(chemin + "/../spill/static/spill") + "/"
    files = ("widget_day","widget_day_mobile")
    widgets = {}
    whost = "theochrone.ga"
    for filename in files:
        with open(fpath + filename) as f:
            widgets[filename] = f.read().format(whost)
    return render(request,'kalendarium/widget.html',locals())

def download(request):
    """View for download page"""
    title = "Télécharger"
    trunk = 'https://theochrone.000webhostapp.com/static/downloads/'
    downloads = {'windows32':trunk + 'windows/theochrone32.zip',
                 'windows64':trunk + 'windows/theochrone64.zip',
                 'linux32':trunk + 'linux/theochrone32',
                 'linux64':trunk + 'linux/theochrone64',
                 'osx32':trunk + 'osx/theochrone32',
                 'osx64':trunk + 'osx/theochrone64',
                 'python':trunk + 'python/Theochrone.zip',
                 } # list of downloads
    return render(request,'kalendarium/download.html',locals())


