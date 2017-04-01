#!/usr/bin/python3
# -*-coding:Utf-8 -*

import calendar
import datetime
import os
import pickle
import re
import shutil
import sys
import unicodedata
from messages import officia_messages as msg
chemin = os.path.dirname(os.path.abspath(__file__))

# variables

unites = (re.compile(r'(1(ere?)?|premiere?)'), # tenter de rajouter un : attention au |
            re.compile('(2(nd)?|second|deux)(.?eme)?'),
            re.compile('(3|trois)(.?eme)?'),
            re.compile('(4|quatre?)(.?eme)?'),
            re.compile('(5|cinqu?)(.?eme)?'),
            re.compile('(6|six)(.?eme)?'),
            re.compile('(7|sept[^u])(.?eme)?'), # le [^u] pose problème # TODO faire des tuples (regex-résultat) ?
            re.compile('(8|huit)(.?eme)?'),
            re.compile('(9|neu[fv])(.?eme)?'),)
dizaines = (re.compile('(11|onze?)(.?eme)?'),
            re.compile('(12|douze?)(.?eme)?'),
            re.compile('(13|treize?)(.?eme)?'),
            re.compile('(14|quatorze?)(.?eme)?'),
            re.compile('(15|quinze?)(.?eme)?'),
            re.compile('(16|seize?)(.?eme)?'),
            re.compile('(17|dix.?.?sept)(.?eme)?'),
            re.compile('(18|dix.?.?huit)(.?eme)?'),
            re.compile('(19|dix.?.?neu[vf])(.?eme)?'),)
vingtaines = (re.compile('(22|vingt.?.?deux)(.?eme)?'),
            re.compile('(23|vingt.?.?trois)(.?eme)?'),
            re.compile('(24|vingt.?.?quatr.?)(.?eme)?'),
            re.compile('(25|vingt.?.?cinq)(.?eme)?'),
            re.compile('(26|vingt.?.?six)(.?eme)?'),
            )
vingt = re.compile('(20|vingt)(.?eme)?')
vingt1 = re.compile('(21|vingt.?.?(et)?.?.?un)(.?eme)?')
dix = re.compile('(10|dix)(.?eme)?')

semaine = {'francais':['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'],
            'english': ['monday','tuesday','wednesday','tuesday','thursday','saturday','sunday'],
            'latina': ['de Feria secunda','de Feria tertia','de Feria quarta','de Feria quinta', 'de Feria sexta','sabbato','dominica'],
               }
mois = ('janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre')
    
liturgiccal=calendar.Calendar(firstweekday=6)

weeknumber = lambda x : [i for i, week in enumerate(liturgiccal.monthdayscalendar(x.year,x.month)) if x.day in week][0] # first week = 0

erreurs={
    'francais':[
        ['Votre interpréteur de commandes n\'est pas compatible avec ce programme. Merci de rentrer la langue manuellement.',
         "Cette fonctionnalité n'a pas encore été implémentée."],
        ["L'année ne peut pas être inférieure à 1600.",
         "L'année ne peut pas être supérieure à 4100.",
         "Merci de rentrer une date valide.",
         "Merci de rentrer un mois valide.",
         "Merci de rentrer un jour qui correspond au mois.",
         "Merci de rentrer un jour de la semaine correspondant au jour du mois.",#5
         "La date de début est postérieure à la date de fin.",
         "Cette semaine est en dehors de l'année demandée.",
         ],
        ["Votre recherche n'a pas pu aboutir. Merci de rentrer des informations plus précises.",],
        ["L'historique des recherches par dates n'a pas encore été renseigné. Merci de faire au moins une recherche.",
         "L'historique des recherches par mots-clefs n'a pas encore été renseigné. Merci de faire au moins une recherche.",
         "Il n'y a pas d'entrée correspondante dans l'historique. Tapez -H pour connaître les entrées disponibles.",],
        ],
    'english':[
        ['Your command-interpreter is not supported by this program.',
         'This functionality has not been implemented yet.'],
        ],
    }
        
# functions

def caracteristiques():
    """Une fonction qui traite les arguments rentrés pour une recherche par caractéristiques (liste de messes votives, de lundis, de fêtes transférées, par couleur, etc., et qui renvoie cette liste ?"""
    pass

def sans_accent(mot):
    """Prend des mots avec accents, cédilles, etc. et les renvoie sans, et en minuscules."""
    return ''.join(c for c in unicodedata.normalize('NFD',mot.lower()) if unicodedata.category(c) != 'Mn')


def modification(mots,langue):
    """Modify some words. 'mots' is a list of strings ; 'langue' refers to language to be used.
    Returns 'mots' modified."""

    if langue == 'francais':
        for i,a in enumerate(mots):
                if mots[i] == 'st':
                    mots[i] = 'saint'
                elif mots[i] == 'ste':
                    mots[i] = 'sainte'
                elif mots[i] in ('bhx','bx'):
                    mots[i] = 'bienheureux'
                elif mots[i] in ('bse','bhse'):
                    mots[i] = 'bienheureuse'
                elif mots[i] in ('bses','bhses'):
                    mots[i] = 'bienheureuses'
        
        # vérifier la regex (.|\|){2}? ne semble pas fonctionner correctement
        mots_str = '|'.join(mots)
        mots_str = vingt1.sub('21',mots_str)
        for i,elt in enumerate(vingtaines):
            mots_str = elt.sub(str(i + 22),mots_str)
        mots_str = vingt.sub('20',mots_str)
        for i, elt in enumerate(dizaines):
            mots_str = elt.sub(str(i + 11),mots_str)
        mots_str = dix.sub('10',mots_str)
        for i, elt in enumerate(unites):
            mots_str = elt.sub(str(i + 1),mots_str)
        mots = mots_str.split('|')
    
    else: # english
        erreur('01')
    
    return mots

def erreur(code,langue='english',exit=True):
    """Une fonction qui renvoie un message d'erreur selon la langue et le code employé. Si le code commence par zéro, il faut le mettre entre guillemets."""
    message = erreurs[langue]
    for i in str(code):
        message = message[int(i)]
    if langue == 'francais':
        if exit:
            sys.exit("Erreur n°{} : {} Tapez --help pour plus d'informations.".format(code,message))
        else:
            return "Erreur n° {} : {}".format(code,message)
    else:
        sys.exit("Error {} : {} Please type --help for more information.".format(code,message))


def datevalable(entree,langue='francais',semaine_seule=False,mois_seul=False,annee_seule=False,exit=True):
    """Function used to see whether a list can be converted into datetime or not"""
    aujourdhui=datetime.date.today()
    nonliturgiccal=calendar.Calendar()
    
    passager=[]

    for elt in entree:
        elt = sans_accent(elt)
        elt = re.sub('(^|[0-9])(st|er|nd|rd|th)$',r"\1",elt)
        if '-' in elt:
            elt = elt.split('-')
        elif '/' in elt:
            elt = elt.split('/')
        if isinstance(elt,list):
            passager += elt
        else:
            passager += [elt]
    for i,elt in enumerate(passager):
        if elt == '':
            del(passager[i])
                
    def producteur_de_datte(jour,mois,annee): # beaucoup d'erreurs potentielles
        """A function to create the datetime.date object"""
        if int(annee) > 4100:
            erreur(11,langue,exit)
        elif int(annee) < 1600:
            erreur(10,langue,exit)
        try:
            date = datetime.date(int(annee),int(mois),int(jour))
        except ValueError:
            date = erreur(14,langue,exit)
        return date
    
    def hebdomadaire(nb):
        """A function wich returns True and a datetime.date which is the first day of the week required"""
        for week in liturgiccal.monthdatescalendar(aujourdhui.year,aujourdhui.month):
            if aujourdhui in week:
                return True, week[0] + datetime.timedelta(nb)
            
    def queljour(jour):
        """A function wich returns a number between 0 and 6 (0=Sunday)"""
        for i,day in enumerate(('dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi')):
            if day == jour:
                return i
            
    def jourmois_joursemaine(jour,date):
        """A function which determines wether or not the weekday entered matches with date"""
        wd=-1
        for i,a in enumerate(semaine[langue]):
            if a == jour.lower():
                wd=i
                break
        for week in nonliturgiccal.monthdatescalendar(date.year,date.month):
            for hideux,day in enumerate(week):
                if day == date and hideux != wd:
                    erreur(15,langue,exit)
                        
    if langue == 'francais':
        if len(passager) == 0:
            date = aujourdhui
            
        elif len(passager) == 1:
            if passager[0] == 'demain':
                date = aujourdhui + datetime.timedelta(1)
            elif passager[0] == 'hier':
                date = aujourdhui - datetime.timedelta(1)
            elif passager[0] == 'semaine':
                semaine_seule, date = hebdomadaire(0)
            elif re.fullmatch(r"[0-9]{8}",passager[0]):
                date = producteur_de_datte(passager[0][:2],passager[0][2:4],passager[0][4:])
            elif re.fullmatch(r"[0-9]{4}",passager[0]):
                date = producteur_de_datte(1,1,passager[0])
                annee_seule = True
            elif re.fullmatch(r"[0-3]?[0-9]",passager[0]):
                date = producteur_de_datte(passager[0],aujourdhui.month,aujourdhui.year)
            elif passager[0] in semaine[langue]:
                for week in liturgiccal.monthdatescalendar(aujourdhui.year,aujourdhui.month):
                    if aujourdhui in week:
                        date = week[queljour(passager[0])]
            else:
                mois = mois_lettre(passager[0],langue)
                date = producteur_de_datte(1,mois,aujourdhui.year,)
                mois_seul = True
        
        elif len(passager) == 2:
            if 'semaine' in passager and 'prochaine' in passager:
                semaine_seule, date = hebdomadaire(7)
            elif 'semaine' in passager and 'derniere' in passager:
                semaine_seule, date = hebdomadaire(-7)
            elif 'avant' in passager and 'hier' in passager:
                date = aujourdhui - datetime.timedelta(2)
            elif 'apres' in passager and 'demain' in passager:
                date = aujourdhui + datetime.timedelta(2)
            elif 'mois' in passager and 'prochain' in passager:
                if aujourdhui.month < 12:
                    date = datetime.date(aujourdhui.year,aujourdhui.month + 1,1)
                else:
                    date = datetime.date(aujourdhui.year + 1,1,1)
                mois_seul = True
            elif 'mois' in passager and 'precedent' in passager:
                if aujourdhui.month == 1:
                    date = datetime.date(aujourdhui.year - 1,12,1)
                else:
                    date = datetime.date(aujourdhui.year,aujourdhui.month + 1,1)
                mois_seul = True
            elif passager[0] in semaine[langue] and passager[1] in ('precedent','avant','dernier'):
                date=aujourdhui
                while True:
                    date -= datetime.timedelta(1)
                    if passager[0] == nom_jour(date,langue):
                        break   
            elif passager[0] in semaine[langue] and (passager[1] == 'suivant' or passager[1] == 'prochain'):
                date=aujourdhui
                while True:
                    date += datetime.timedelta(1)
                    if passager[0] == nom_jour(date,langue):
                        break 
            elif passager[0] in semaine[langue] and re.fullmatch(r"[0-3]?[0-9]",passager[1]):
                date = producteur_de_datte(passager[1],aujourdhui.month,aujourdhui.year)
                jourmois_joursemaine(passager[0],date)              
            elif ('an' in passager or 'annee' in passager) and ('prochain' in passager or 'prochaine' in passager):
                date = datetime.date(aujourdhui.year + 1,1,1)
                annee_seule = True
            elif ('an' in passager or 'annee' in passager) and ('dernier' in passager or 'derniere' in passager):
                date = datetime.date(aujourdhui.year - 1, 1,1)
                annee_seule = True
            elif re.fullmatch(r"[0-9]{4}",passager[1]): #janvier 2000, 1 2000
                if not re.fullmatch(r"(1[1-2]|0?[1-9])",passager[0]):
                    passager[0] = mois_lettre(passager[0],langue)
                date = producteur_de_datte(1,passager[0],passager[1])
                mois_seul = True
            elif re.fullmatch(r"[0-3]?[0-9]",passager[0]): # ex: 11 janvier, 11 1
                if not re.fullmatch(r"(1[1-2]|0?[1-9])",passager[1]):
                    passager[1] = mois_lettre(passager[1],langue)
                date = producteur_de_datte(passager[0],passager[1],aujourdhui.year)
            else:#erreur
                erreur(12,langue,exit)
        
        elif len(passager) == 3:
            if passager[0] in semaine[langue]:
                if not re.fullmatch(r"(1[1-2]|0?[1-9])",passager[2]):
                    passager[2] = mois_lettre(passager[2],langue)
                date = producteur_de_datte(passager[1],passager[2],aujourdhui.year)
                jourmois_joursemaine(passager[0],date)
            elif re.fullmatch(r"[0-3]?[0-9]",passager[0]) and re.fullmatch(r"[0-9]{4}",passager[2]):
                if not re.fullmatch(r"(1[1-2]|0?[1-9])",passager[1]):
                    passager[1] = mois_lettre(passager[1],langue)
                    
                date = producteur_de_datte(passager[0],passager[1],passager[2])
            else:#erreur
                erreur(12,langue,exit)
        
        elif len(passager) == 4: # il faut gérer les erreurs
            if not re.fullmatch(r"(1[1-2]|0?[1-9])",passager[0]):
                passager[2] = mois_lettre(passager[2],langue)
            date = producteur_de_datte(passager[1],passager[2],passager[3])
            jourmois_joursemaine(passager[0],date) 
                    
        else: # erreur
            erreur(12,langue,exit)
    else: # english
        pass
    return date, semaine_seule, mois_seul, annee_seule

def AtoZ(semaine_seule,mois_seul,annee_seule,date):
    """Une fonction qui définit le début et la fin de la période qui va être affichée"""
    if semaine_seule:
        debut = date
        fin = date + datetime.timedelta(6)
    elif annee_seule:
        debut = date
        fin = datetime.date(date.year,12,31)
    elif mois_seul:
        debut = date
        fin = datetime.date(date.year,date.month,calendar.monthrange(date.year,date.month)[1])
    else:
        debut = date
        fin = date
    
    return debut, fin

def mois_lettre(mot,langue='english'):
    """Une fonction qui doit déterminer si le mot entré correspond à un mois. Si le mot entré correspond à un chiffre, renvoie le nom du mois ; si le mot entré est un nom de mois, vérifie qu'il en est un et renvoie le chiffre correspondant."""
    if isinstance(mot,str):
        mot = mot.lower()
    if langue == 'francais':
        if isinstance(mot,int):
            return mois[mot - 1]
        for i,a in enumerate(mois):
            if mot.lower() in sans_accent(a):
                return i + 1
        erreur(13,langue)
    else: #default : english
        for month_idx in range(1,13):
            if mot in calendar.month_name[month_idx].lower():
                return True, str(month_idx)
    return False, 0
     


def renvoie_regex(retour,regex,liste):
    retour.__dict__['regex'] = {}
    de_cote = []
    for index in regex:
        retour.regex[index]=[]
        for a in regex[index]:
            for elt in liste:
                if a.match(str(elt)):
                    de_cote.append(a)
                else:
                    retour.regex[index].append(a)
    retour.regex['egal'] += de_cote
    return retour

def affiche_temps_liturgique(objet,Annee,langue='francais'):
    """Une fonction capable d'afficher le temps liturgique"""
    sortie = 'erreur'
    if langue == 'francais':
        if objet.temps_liturgique(Annee) == 'nativite':
            sortie = "temps de la Nativité (Temps de Noël)"
        elif objet.temps_liturgique(Annee) == 'epiphanie':
            sortie = "temps de l'Épiphanie (Temps de Noël)"
        elif objet.temps_liturgique(Annee) == 'avent':
            sortie = "temps de l'Avent"
        elif objet.temps_liturgique(Annee) == 'apres_epiphanie':
            sortie = "temps per Annum après l'Épiphanie"
        elif objet.temps_liturgique(Annee) == 'septuagesime':
            sortie = "temps de la Septuagésime"
        elif objet.temps_liturgique(Annee) == 'careme':
            sortie = "temps du Carême proprement dit (Temps du Carême)"
        elif objet.temps_liturgique(Annee) == 'passion':
            sortie = "temps de la Passion (Temps du Carême)"
        elif objet.temps_liturgique(Annee) == 'paques':
            sortie = "temps de Pâques (Temps Pascal)"
        elif objet.temps_liturgique(Annee) == 'ascension':
            sortie = "temps de l'Ascension (Temps Pascal)"
        elif objet.temps_liturgique(Annee) == 'octave_pentecote':
            sortie = "octave de la Pentecôte (Temps Pascal)"
        elif objet.temps_liturgique(Annee) == 'pentecote':
            sortie = "temps per Annum après la Pentecôte"
    else: # english
        pass
    return sortie

def affiche_jour(date,langue):
    """Une fonction pour afficher le jour"""
    if langue =='francais':
        if date.day == 1:
            jour = 'premier'
        else:
            jour = date.day
        mois = mois_lettre(date.month,langue)
        sortie="""le {} {} {} {}""".format(nom_jour(date,langue),jour,mois,date.year)
    elif kwargs['langue']=='english':
        sortie="""on {}""".format(date)
    elif kwargs['langue']=='latina':
        sortie="""in {}""".format(date) # à développer
    
    return sortie

def affichage(**kwargs):
    """Une fonction destinée à l'affichage des résultats."""
    if kwargs['verbose'] and not kwargs['recherche']:
        sortie = affiche_jour(kwargs['date'],kwargs['langue']).capitalize() + ' :'
    else:
        sortie=''
    for a in kwargs['liste']:
        if a.omission and not kwargs['verbose'] and not kwargs['recherche']:
            """if sortie [-2:] == '\n': # ne marche toujours pas
                sortie = sortie[:-2]"""
            continue
        elif sortie != '':
            sortie += "\n"
        if kwargs['langue'] == 'francais':
            if kwargs['verbose']:
                if a.celebree:
                    attente = 'on célèbre '
                elif a.peut_etre_celebree and a.commemoraison:
                    attente = 'on peut célébrer ou commémorer '
                elif a.peut_etre_celebree and not a.celebree:
                    attente = 'on peut célébrer '
                elif a.commemoraison:
                    attente = 'on commémore '
                elif a.omission:
                    attente = 'on omet '
                    
                if sortie[-1:] == '\n' or sortie[-1:] == '':
                    sortie += attente.capitalize()
                else:
                    sortie += attente
                    
                for i, mot in enumerate(a.nom['francais'].lower().split()): # TODO faire plutôt des regex : bien plus précis
                    if [True for i in ('dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi','jour') if i in mot]:
                        sortie += 'le '
                        break
                    elif [True for i in ('dédicace','présentation','fête','très','commémoraison','vigile') if i in mot]:
                        sortie += 'la '
                        break
                    elif [True for i in ('saints',) if i in mot]:
                        sortie += 'les '
                        break
                    elif [True for i in ('office','octave','épiphanie') if i in mot]:
                        sortie += "l'"
                        break
                    if i > 2:
                        break
            
            if kwargs['date_affichee'] and not kwargs['verbose'] and not kwargs['recherche']:
                sortie += """{}/{}/{} """.format(kwargs['date'].day,kwargs['date'].month,kwargs['date'].year)
                if kwargs['jour_semaine']:
                    sortie += '(' + nom_jour(a.date,kwargs['langue']) + ') '
            
            if kwargs['jour_semaine'] and not kwargs['verbose'] and not kwargs['recherche'] and not kwargs['date_affichee']:
                sortie += nom_jour(a.date,kwargs['langue']).capitalize() + ' '
                
            if (kwargs['jour_semaine'] or kwargs['date_affichee']) and not kwargs['recherche'] and not kwargs['verbose']:
                sortie += ': '
                
            sortie += a.nom['francais']
            
            if not kwargs['verbose'] and a.commemoraison:
                sortie += ' (Commémoraison)'
            elif not kwargs['verbose'] and kwargs['recherche'] and a.omission:
                sortie += ' (omis)'
                
            if kwargs['recherche'] and kwargs['verbose']:
                sortie += ' ' + affiche_jour(a.date,kwargs['langue'])
                
            if kwargs['recherche'] and not kwargs['verbose']:
                sortie += """ : {}/{}/{}""".format(a.date.day,a.date.month,a.date.year)
            
            if kwargs['recherche'] and not kwargs['verbose'] and kwargs['jour_semaine']:
                sortie += ' (' + nom_jour(a.date,kwargs['langue']) + ')'
                
            sortie += '. '
            
            if kwargs['verbose'] or kwargs['degre']:
                if a.degre == 1:
                    sortie += """Fête de première classe. """
                elif a.degre == 2:
                    sortie += """Fête de deuxième classe. """
                elif a.degre == 3:
                    sortie += """Fête de troisième classe. """
                elif a.degre == 4:
                    sortie += """Fête de quatrième classe. """
                else:
                    sortie += """Commémoraison. """
                    
            if kwargs['verbose'] or kwargs['transfert']:                    
                if a.transferee:
                    origine = a.date_originelle
                    if origine.day == 1:
                        jour = 'premier'
                    else:
                        jour = origine.day
                    mois = mois_lettre(a.date_originelle.month,kwargs['langue'])
                    sortie += """Fête transférée du {} {} {}. """.format(jour, mois, origine.year)
                  
            if kwargs['verbose'] or kwargs['temporal_ou_sanctoral']:
                if a.temporal:
                    sortie += """Fête du Temps. """
                else:
                    sortie += """Fête du Sanctoral. """
                    
            if kwargs['verbose'] or kwargs['temps_liturgique']:
                sortie += """Temps liturgique : {}. """.format(affiche_temps_liturgique(a,kwargs['Annee'],'francais'))
                
            if kwargs['verbose'] or kwargs['couleur']:
                sortie += """Couleur liturgique : {}. """.format(a.couleur)
            
            if kwargs['verbose']:
                sortie += a.addendum[kwargs['langue']]
                
        elif kwargs['langue'] == 'english':
            erreur('01')
        else: # latin
            pass
        """if a != kwargs['liste'][-1]:
            sortie += '\n'"""
            
    return sortie
            



def nom_jour(date,langue):
    """Une fonction qui renvoie le nom du jour de la semaine en fonction du datetime.date rentré"""
    return semaine[langue][datetime.date.weekday(date)]                    




def dimancheavant(jour):
    """Une fonction qui renvoie le dimanche d'avant le jour concerné. jour doit être un datetime.date."""
    return jour - datetime.timedelta(datetime.date.isoweekday(jour))
    
def dimancheapres(jour):
    """Une fonction qui renvoie le dimanche d'après le jour concerné. jour doit être un datetime.date."""
    ecart=datetime.timedelta(7 - datetime.date.isoweekday(jour))
    return jour + ecart if ecart.days != 0 else jour + datetime.timedelta(7)
    
def weekyear(year, week=None):
    """
    This function returns the first and the later day of a weekyear.
    It takes two integers as arguments : a year 
    and a week number in the year (ex : 2017, 2).
    It returns two datetime.date objects : 
    the first one is always a Sunday and may be, 
    if it is in the week 0, in the past year ; 
    the second one is the Saturday following this Sunday.
    This function uses the ISO format of the year, 
    but assumes that the first weekday is Sunday, the last Saturday. 
    However, calculus is made on the base of a week 
    starting with Monday, and is moved just later.
    Week 0 is the last week of the previous year, if it exists.
    If January 1st is a Sunday, week 0 does not exist,
    and a request for it in this case will return week 1.
    If week=None, returns the number of weeks in the year
    according to this system.
    Function inspired by this page : http://code.activestate.com/recipes/521915-start-date-and-end-date-of-given-week/
    """
    firstday = datetime.date(year, 1, 1)
    if firstday.weekday() > 3:
        firstday = firstday + datetime.timedelta(7 - firstday.isoweekday())
    else:
        firstday = firstday - datetime.timedelta(firstday.isoweekday())
    weeknumber = int(((datetime.date(year,12,31) - firstday).days / 7) + 1)
    if week == None:
        return weeknumber
    if week < 0 or week > weeknumber:
        erreur(17,langue='francais')
    gap = datetime.timedelta(days = (week - 1)*7)
    start = firstday + gap
    end = firstday + gap + datetime.timedelta(6)
    if week == 0 and end.year != year:
        start, end = weekyear(year, 1)
    return start, end



def inversons(mots_bruts,Annee,debut,fin,plus=False,langue='francais',exit=True):
    """Function which returns a list of feasts matching with mots_bruts. It takes six args:
    - mots_bruts : a string for the research ;
    - Annee : a dict with datetime.date as keys, and lists of Fete as values ;
    - debut : a datetime.date for the older date ;
    - fin : a datetime.date for the latest date ;
    - samedi : the Saturday of the Virgin Fete ; # DEPRECATED no more useful
    - plus : a bool to define whether the results will be larger or not ;
    - langue : language used ;
    - exit : a bool to define whether the system have to exit or not in case of error ;
    """
    if isinstance(mots_bruts,list):
        mots_bruts = [sans_accent(mot) for mot in mots_bruts]
    else:
        mots_bruts = sans_accent(mots_bruts).split()
    mots = []
    for mot in mots_bruts:
        if ' ' in mot:
            mots = mots + mot.split()
        else:
            mots = mots + [mot]
    mots = modification(mots,langue)
    mots_str=''
    for a in mots:
        mots_str += a
        
    boucle = True
    date = debut
    if date == fin:
        date = datetime.date(date.year,1,1)
        fin = datetime.date(date.year,12,31)
    retenus = []
    while date <= fin:
        try:
            for fete in Annee[date]:
                fete.valeur = fete.Correspondance(mots_str,mots,plus)
                if fete.valeur >= 50:
                    retenus.append(fete)
        except KeyError:
            pass
        date += datetime.timedelta(1)
    
    retenus.sort(key=lambda x:x.valeur,reverse=True)
    superieurs = [x for x in retenus if x.valeur >= 70 and x.valeur < 100]
    elite = [x for x in retenus if x.valeur >= 100]
    if plus:
        liste = retenus
    elif len(elite) >= 1:
        liste = elite
    elif len(superieurs) >= 1:
        liste=superieurs
    elif len(superieurs) == 0 and len(retenus) >= 1:
        liste=retenus
    else:
        liste = [erreur(20,langue,exit=exit)]
    
    return liste

def pdata(read=True,write=False,**kwargs):
    """A function for personal data, which reads and writes config files and history in ~/.theochrone"""
    main_folder = os.path.expanduser('~/.theochrone')
    config_folder = main_folder + '/config'
    history_folder = main_folder + '/history'
    
    if not os.path.exists(main_folder):
        os.mkdir(main_folder)
        os.mkdir(config_folder)
        os.mkdir(history_folder)
        with open(main_folder + '/SET','w') as SETfile:
            SETfile.write('ON')
        
    if 'SET' in kwargs:
        with open(main_folder + '/SET','w') as SETfile:
            if kwargs['SET'] == 'OFF':
                SETfile.write('OFF')
                for folder in (config_folder,history_folder,):
                    try:
                        shutil.rmtree(folder)
                    except FileNotFoundError:
                        pass
            else:
                SETfile.write('ON')
                for folder in (config_folder,history_folder,):
                    try:
                        os.mkdir(folder)
                    except FileExistsError:
                        pass
                
    with open(main_folder + '/SET','r') as SETfile:
        if 'OFF' in SETfile.read():
            return [] # WARNING très mauvaise idée : cela évite juste les ennuis, mais ne résout rien !!! renvoyer plutôt False
        
    if kwargs.get('langue',False):
        with open(config_folder + '/LANG','w') as lang:
            lang.write(kwargs['langue'])
    
    if write:
        action = 'a'
    else:
        action = 'r'
        
    if 'history' in kwargs:
        aujourdhui = str(datetime.datetime.today())
        if kwargs['history'] == 'dates':
            if not write:
                if not os.path.isfile(history_folder + '/dates'):
                    erreur(30,'francais')               
            with open(history_folder + '/dates',action) as dates:
                if write:
                    if kwargs.get('semaine_seule',False):
                        periode = 'week'
                    elif kwargs.get('mois_seul',False):
                        periode = 'month'
                    elif kwargs.get('annee_seule',False):
                        periode = 'year'
                    elif kwargs.get('fromto',False):
                        periode = 'arbitrary'
                    else:
                        periode = 'day'
                        
                    debut = kwargs['debut'].strftime("%Y-%m-%d")
                    fin = kwargs['fin'].strftime("%Y-%m-%d")
                    
                    dates.write('{}<>{}<>{}|{}\n'.format(aujourdhui,periode,debut,fin))
                else:
                    history = []
                    
                    for line in dates.readlines():
                        tmp = []
                        separee = line.replace('\n','').split('<>')
                        tmp.append(datetime.datetime.strptime(separee[0],'%Y-%m-%d %H:%M:%S.%f'))
                        tmp.append(separee[1])
                        tmp.append([datetime.datetime.strptime(date,'%Y-%m-%d').date() for date in separee[2].split('|')])
                        history.append(tmp)
                    return history
        elif kwargs['history'] == 'reverse':
            if not write:
                if not os.path.isfile(history_folder + '/keywords'):
                    erreur(31,'francais')
            with open(history_folder + '/keywords',action) as keywords:
                if write:
                    debut = kwargs['debut'].strftime("%Y-%m-%d")
                    fin = kwargs['fin'].strftime("%Y-%m-%d")
                    keywords.write("""{}/{}|{}/{}\n""".format(aujourdhui,debut,fin,' '.join(kwargs['keywords'])))
                else:
                    history = []
                    for line in keywords.readlines():
                        jour, dates, kw = line.split('/')
                        history.append([datetime.datetime.strptime(jour,'%Y-%m-%d %H:%M:%S.%f')] +                                                                 [datetime.datetime.strptime(date,'%Y-%m-%d').date() for date in dates.split('|')] + [kw.replace('\n','').split()])
                    return history
    return True
                    
            


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
