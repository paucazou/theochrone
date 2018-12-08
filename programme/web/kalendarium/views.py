from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
import calendar
import datetime
import io
import os
import sys
from .forms import * 


# Create your views here.

chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/../..')
sys.path.append(programme)
import annus
import adjutoria
import exporter
import martyrology
import officia

martyrology_instance = martyrology.Martyrology()
host = os.environ.get("THEHOST","localhost:8000")
liturgical_calendar = annus.LiturgicalCalendar(proper='roman')
s=os.environ.get("SECURE",'')
if s is None:
    s='s'
    
#load raw widgets
fpath = os.path.abspath(chemin + "/../spill/static/spill") + "/"
unformated_widgets = {}
for filename in ("widget_day","widget_day_mobile"):
    with open(fpath + filename) as f:
        unformated_widgets[filename] = f.read()

def home(request,
         recherche_mot_clef=RechercheMotClef(None),recherche_simple=RechercheSimple(None),mois_entier=MoisEntier(None),mois_seul=False,
         debut=None,fin=None,pal=False,
         proper='roman',
         mots_clefs='',plus=False,annee=None):
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
    if proper not in propers:
        proper = 'roman'
    liturgycal = annus.LiturgicalCalendar(proper=proper)
    retour = ''
    deroule = {}
    if debut == None:
        debut = datetime.date.today()
    if fin == None:
        fin = datetime.date.today()
    if mots_clefs == '':
        hashtag = 'resultup'
        if debut == fin: #à mettre dans le template
            next_item = officia.datetime_to_link(fin + datetime.timedelta(1),host,hashtag=hashtag,s=s,proper=proper,pal=pal)
            previous_item = officia.datetime_to_link(debut - datetime.timedelta(1),host,hashtag=hashtag,s=s,proper=proper,pal=pal)
        else:
            next_item = officia.month_to_link(fin,host,1,hashtag,s,proper)
            previous_item = officia.month_to_link(debut,host,-1,hashtag,s,proper)
        date = debut
        liturgycal(date.year)
        while date <= fin:
            deroule[date] = liturgycal[date]
            date = date + datetime.timedelta(1)
        inversion=False
        if mois_seul:
            titre = officia.mois[debut.month - 1]
        else:
            titre = debut
    else:
        if annee is None:
            annee = datetime.date.today().year
        titre = mots_clefs
        liturgycal(annee)
        try:
            deroule[titre] = officia.inversons(mots_clefs,liturgycal,datetime.date(annee,1,1),datetime.date(annee,12,31),langue='fr',exit=True,plus=plus)
        except SystemExit:
            deroule[titre] = []
        inversion=True

    #values for templates
    for value in deroule.values():
        for elt in value:
            liturgical_time = officia.affiche_temps_liturgique(elt,lang='fr')
            elt.temps_liturgique_ = liturgical_time[0].upper() + liturgical_time[1:]
            elt.proper_ = propers[elt.propre]
    shared_research = _setSharedResearch(pal=pal,martyrology=False,proper=proper)
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
            pal = recherche_mot_clef.cleaned_data['pal']
            proper = recherche_mot_clef.cleaned_data['proper']
            result = home(request,recherche_mot_clef,mots_clefs=mots_clefs,plus=plus,pal=pal,annee=annee,proper=proper)
    else:
        result = home(request, recherche_mot_clef)
    return result
        
def date_transfert(request):
    """A function which takes the request arguments (GET) and returns the home function with the results of a research by date"""
    recherche_simple = RechercheSimple(request.GET or None)
    if recherche_simple.is_valid():
        date = recherche_simple.cleaned_data['date_seule']
        pal = recherche_simple.cleaned_data['pal']
        proper = recherche_simple.cleaned_data['proper']
        if recherche_simple.cleaned_data['martyrology']:
            result = martyrology_date(request,date,recherche_simple)
        else:
            result = home(request,recherche_simple=recherche_simple,debut=date,fin=date,pal=pal,proper=proper)
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
        fin = datetime.date(annee,mois,calendar.monthrange(annee,mois)[1])
        pal = mois_entier.cleaned_data['pal']
        proper = mois_entier.cleaned_data['proper']
        return home(request,mois_entier=mois_entier,mois_seul=True,pal=pal,debut=debut,fin=fin,proper=proper)
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
    result_len = len(result)
    shared_research = _setSharedResearch(martyrology=True)
    return render(request,'kalendarium/accueil.html',locals())

def martyrology_kw(request,recherche_mot_clef=None):
    """Return martyrology for a keyword research"""
    inversion = martyrology = True
    keywords = recherche_mot_clef.cleaned_data['recherche']
    max_nb_returned = [10,5][not recherche_mot_clef.cleaned_data['plus']]
    result = martyrology_instance.kw(keywords.split(),'fr',max_nb_returned=max_nb_returned,year=recherche_mot_clef.cleaned_data['annee'])
    mois_entier=MoisEntier(None)
    recherche_simple=RechercheSimple(None)
    hashtag = 'resultup'
    credits = martyrology_instance.credits('fr')
    titre = "Martyrologe romain : {}".format(keywords)
    result_len = len(result)
    shared_research = _setSharedResearch(martyrology=True)
    return render(request,'kalendarium/accueil.html',locals())
    
# contact
def contact(request):
    """A function which takes the request arguments (POST)
    and returns the view with success"""
    contact_success = False
    titre = "Contact"
    other_apps = (
        ('Divinum Officium, le plus complet','http://divinumofficium.com/'),
        ('Chant grégorien','http://www.chantgregorien.free.fr/calendrier/calend.php'),
        ('Per Ipsum','https://peripsum.org/peripsum.php'),
        ('1962 Ordo (FSSPX, en anglais)','https://1962ordo.today/'),
        )
    partners = (
        ('Tradinews','http://tradinews.blogspot.fr/'),
        ('Metablog','https://ab2t.blogspot.fr/'),
        ('Le Salon Beige','https://www.lesalonbeige.fr/#theocontainer'),
        ('BLH Land','http://www.blh-land.fr/#theocontainer'),
        ('Contre Info','http://www.contre-info.com/'),
        ("Association Saint Florent d'Anjou",'https://saint-florent-anjou.fr/#theocontainer'),
        ) # Mettre cela ailleurs. Où ? TODO
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
    widgets = { filename:widget.format(s,host) for filename,widget in unformated_widgets.items() }
    # templates variables
    options_day = OptionsWidgetDay()
    options_day_mobile = OptionsWidgetDayMobile()
    return render(request,'kalendarium/widget.html',locals())

def download(request):
    """View for download page"""
    title = "Télécharger"
    VERSION = "0.6.0"
    trunk = "https://github.com/paucazou/theochrone/releases/download/v{}/".format(VERSION)
    downloads = {'windows32':trunk + 'theochrone_windows32.zip',
                 'windows64':trunk + 'theochrone_windows64.zip',
                 'linux32':trunk + 'theochrone_linux32.zip',
                 'linux64':trunk + 'theochrone_linux64.zip',
                 'osx':trunk + 'theochrone_osx.zip', 
                 'python':trunk + 'theochrone.zip',
                 } # list of downloads
    # variables for template
    export_form = ExportResults(request.GET or None)
    return render(request,'kalendarium/download.html',locals())

def export(request):#TODO passer cette fonction en statique, ou de telle manière que cloudflare l'enregistre
    """Export the data to ICS or CSV format"""
    export_request = ExportResults(request.GET or None)
    if export_request.is_valid():
        # prepare data
        data = export_request.cleaned_data
        year = data['year']
        start = datetime.date(year,1,1)
        end = datetime.date(year,12,31)
        # export
        stream = io.StringIO()
        exporter.main(start,end,'fr',stream,
                proper=data['proper'],
                file_ext=data['format'],
                pal=data['pal'])

        #filename
        pal_filename_details = "_PAL" if data['pal'] else ''
        filename = "Theochrone_{}_{}{}.{}".format(year,data['proper'],pal_filename_details,data['format'])
        print('Stream: ',stream.read())

        #response
        response = HttpResponse(stream.getvalue(),content_type='type/{}'.format(data['format'])) # type calendar for ics ??
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response
    else:
        return download(request)

def _setSharedResearch(martyrology=False,pal=False,proper='roman') -> SharedResearch:
    """Set the shared research form"""
    values = {'pal':pal,
            'martyrology':martyrology,
            'proper':proper}
    return SharedResearch(initial=values)


