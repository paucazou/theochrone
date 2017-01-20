#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
import datetime
import calendar
import pickle
import subprocess
import argparse
import sys
import unicodedata
import re
import copy
#import pdb ; pdb.set_trace()
#from IPython.lib.deepreload import reload as dreload

# Deus, in adjutorium meum intende.

# variables

unites = (re.compile('(1(er)?|un|premier)'),
            re.compile('(2(nd)?|second|deux)(.?eme)?'),
            re.compile('(3|trois)(.?eme)?'),
            re.compile('(4|quatre?)(.?eme)?'),
            re.compile('(5|cinqu?)(.?eme)?'),
            re.compile('(6|six)(.?eme)?'),
            re.compile('(7|sept)(.?eme)?'),
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
        
fichiers=(
    'romanus_1962_dimanches',
    'romanus_1962_fetesduseigneur',
    'romanus_1962_cycledenoel',
    #'romanus_1962_saints_premier_trimestre',
    #'gallicanus_1962_dimanches',
    #'samedi', ce fichier n'est utilisé que dans un cas particulier.
    )

latinus={
    'romanus':{
        'gallicanus':{
            'lugdunensis':{},
            'parisianus':{},
            },
        'italianus':{},
        'testis':{}, # a test proper, only used with the --test arg.
        },
        'dominicanus':{},
        'cartusiensis': {},
        'visigothica':{},
        'ambrosianus':{},
        'cisterciensis':{},
        'bracarenses':{},
        } # contains the pyramid of the propers ; used in the 'remonte' and 'trouve' functions    

erreurs={
    'francais':[
        ['Votre interpréteur de commandes n\'est pas compatible avec ce programme. Merci de rentrer la langue manuellement.',
         "Cette fonctionnalité n'a pas encore été implémentée."],
        ["L'année ne peut pas être inférieure à 1583.",
         "L'année ne peut pas être supérieure à 4100.",
         "Merci de rentrer la date sous une forme standard comme JJ-MM-AAAA.",
         "Merci de rentrer un jour ou un mois valide."]
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

def ocasu():
    """Go to http://philippeaucazou.wordpress.com"""
    try:
        subprocess.run(['x-www-browser','http://philippeaucazou.wordpress.com'],check=True)
    except:
        subprocess.run(['www-browser','http://philippeaucazou.wordpress.com'],check=True)
    sys.exit()

def modification(mots,langue):
    """Change certains mots"""

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
        
        mots_str='' # supprimer le | initial ; vérifier la regex (.|\|){2}? ne semble pas fonctionner correctement
        for a in mots:
            mots_str = mots_str + '|' + a
        
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
        del(mots[0])
    
    else: # english
        erreur('01')
    
    return mots

def erreur(code,langue='english'):
    """Une fonction qui renvoie un message d'erreur selon la langue et le code employé. Si le code commence par zéro, il faut le mettre entre guillemets."""
    message = erreurs[langue]
    for i in str(code):
        message = message[int(i)]
    if langue == 'francais':
        sys.exit("Erreur n°{} : {} Tapez --help pour plus d'informations.".format(code,message))
    else:
        sys.exit("Error {} : {} Please type --help for more information.".format(code,message))

def default_language():
    """Find which language is used on the system"""
    shell, err = subprocess.Popen('echo $SHELL', stdout=subprocess.PIPE, shell=True).communicate()
    shell = str(shell)
    
    if 'sh' in shell: # fonctionnera pour tout interpréteur type sh, bash, zsh, tcsh, etc.
         command = 'printenv LANGUAGE'
    else:
        erreur('00')
    
    langue_defaut, error=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()
    
    if b'fr' in langue_defaut:
        langue_defaut = 'francais'
    else:
        langue_defaut = 'english'
    
    return langue_defaut

def datevalable(entree,langue_defaut='english',mois_seul=False,annee_seule=False):
    """Function used to see whether a list can be converted into datetime or not"""
    aujourdhui=datetime.date.today()
    
    if "-" in entree[0]:
        entree=entree[0].split('-')
    elif '/' in entree[0]:
        entree=entree[0].split('/')
    
    for i, elt in enumerate(entree):
        entree[i] = re.sub('(^|[0-9])(st|er|nd|rd|th)$',r"\1",entree[i])
        if entree[i] == '':
            del(entree[i])
            
    if len(entree) == 1:
        try:
            if int(entree[0]) >= 1583 and int(entree[0]) <= 4100:
                if langue_defaut == 'francais':
                    entree = ['1','1',entree[0]]
                else:
                    entree = [entree[0], '1', '1']
                annee_seule = True
        except ValueError:
            pass
        
    if len(entree) < 3:
        mois_seul, mois = mois_lettre(entree[0],langue_defaut)
        if mois_seul:
            entree[0] = mois
            if langue_defaut == 'francais':
                entree = ['1'] + entree
            else:
                entree = entree + ['1']
    try:
        assert len(entree) < 4
        if len(entree) == 1 and len(entree[0]) == 8:
            entree = entree[0]
            if langue_defaut == 'francais':
                jour = int(entree[:2])
                mois = int(entree[2:4])
                an = int(entree[4:])
            else:
                jour = int(entree[6:])
                mois = int(entree[4:6])
                an = int(entree[:4])
            return datetime.date(an,mois,jour)
        
        entree = [int(a) for a in entree]
        if len(entree) == 1:
            date=datetime.date(aujourdhui.year,aujourdhui.month,entree[0])
        elif langue_defaut == 'francais':
            if len(entree) == 2:
                date=datetime.date(aujourdhui.year,entree[1],entree[0])
            else:
                date=datetime.date(entree[2],entree[1],entree[0])
        else: # default : english format
            if len(entree) == 2:
                date=datetime.date(aujourdhui.year,entree[0],entree[1])
            else:
                date=datetime.date(entree[0],entree[1],entree[2])
    except AssertionError:
        erreur(12,langue_defaut)        
    except ValueError:
        try:
            if langue_defaut == 'francais':
                retour, chiffre = mois_lettre(entree[1],'francais')
                if retour:
                    entree[1] = chiffre
            else:
                for i, a in enumerate(entree):
                    retour, chiffre = mois_lettre(a)
                    if retour and len(entree) == 2:
                        entree = [str(aujourdhui.year)] + [chiffre] + [entree[1]]
                        break
                    elif retour and len(entree) == 3:
                        entree = [str(aujourdhui.year)] + [chiffre] + [entree[0]]
                        break
            if not retour:
                erreur(13,langue_defaut)
            else:
                date, mois_seul, annee_seule = datevalable(entree,langue_defaut,mois_seul,annee_seule)
        except AttributeError:
            erreur(12,langue_defaut)
        except TypeError:
            erreur(12,langue_defaut)
            
    return date, mois_seul, annee_seule

def mois_lettre(mot,langue='english'):
    """Une fonction qui doit déterminer si le mot entré correspond à un mois. Si le mot entré correspond à un chiffre, renvoie le nom du mois ; si le mot entré est un nom de mois, vérifie qu'il en est un et renvoie un booléen et le chiffre correspondant."""
    if isinstance(mot,str):
        mot = mot.lower()
    if langue == 'francais':
        mois = (
            (1,'janvier'),
            (2,'février','fevrier'),
            (3,'mars'),
            (4,'avril'),
            (5,'mai'),
            (6,'juin'),
            (7,'juillet'),
            (8, 'août','aout'),
            (9,'septembre'),
            (10,'octobre'),
            (11,'novembre'),
            (12, 'décembre','decembre')
            )
        if isinstance(mot,int):
            return mois[mot][1]
        for a in mois:
            for f in a[1:]:
                if mot.lower() in f:
                    return True, str(a[0])
    else: #default : english
        for month_idx in range(1,13):
            if mot in calendar.month_name[month_idx].lower():
                return True, str(month_idx)
    return False, 0
     

def traite(Annee,objet,date,annee,propre):
    """Déplace la fête 'objet' si c'est nécessaire."""
    try:
        isinstance(Annee[date],list)
    except KeyError:
        Annee[date]=[objet]
        return Annee
    #Faut-il déplacer ?
    adversaire = Annee[date][0]
    # Cas de 'objet' ayant la même self.personne que 'adversaire'
    if objet.personne == adversaire.personne:
        Annee[date].append(objet)
    # Cas de 'objet' et 'adversaire' tous deux transférés
    elif objet.transferee and adversaire.transferee:
        if objet.priorite > adversaire.priorite:
            Annee[date][0] = objet
            adversaire.date = adversaire.date + datetime.timedelta(1)
            adversaire.transferee=True
            Annee=traite(Annee,adversaire,date + datetime.timedelta(1),annee)
        else:
            objet.date = objet.date + datetime.timedelta(1)
            Annee=traite(Annee,objet,date + datetime.timedelta(1),annee)
    # Si l'un ou l'autre est transféré
    elif objet.transferee and adversaire.priorite > 800:
        objet.date = objet.date + datetime.timedelta(1)
        Annee=traite(Annee,objet,date + datetime.timedelta(1),annee)
    elif adversaire.transferee and objet.priorite > 800:
        Annee[date][0] = objet
        adversaire.date = adversaire.date + datetime.timedelta(1)
        Annee=traite(Annee,adversaire,date + datetime.timedelta(1),annee)
    # Cas de 'objet' fête de première classe vs 'adversaire' fête de première classe
    elif objet.priorite > 1600:
        if objet.priorite < adversaire.priorite and not objet.dimanche:
            objet.transferee=True
            objet.date = objet.date + datetime.timedelta(1)
            Annee=traite(Annee,objet,date + datetime.timedelta(1),annee)
        elif adversaire.priorite > 1600 and adversaire.priorite < objet.priorite and not adversaire.dimanche:
            Annee[date][0] = objet
            adversaire.date = adversaire.date + datetime.timedelta(1)
            adversaire.transferee=True
            Annee=traite(Annee,adversaire,date + datetime.timedelta(1),annee)
    elif propre != 'romanus' and (objet.occurrence_perpetuelle or adversaire.occurrence_perpetuelle):
        premier_dimanche_avent = dimancheapres(datetime.date(annee,12,25)) - datetime.timedelta(28)
        # Cas de 'objet' fête de seconde classe empêchée perpétuellement
        if objet.priorite > 800 and adversaire.priorite > 800 and adversaire.priorite > objet.priorite and not objet.dimanche:
            objet.date = objet.date + datetime.timedelta(1)
            Annee=traite(Annee,objet, date + datetime.timedelta(1),annee)
        elif adversaire.priorite > 800 and objet.priorite > 800 and objet.priorite > adversaire.priorite and not adversaire.dimanche:
            Annee[date][0] = objet
            adversaire.date = adversaire.date + datetime.timedelta(1)
            Annee=traite(Annee,adversaire,date + datetime.timedelta(1),annee)
        # Cas de 'objet' fête de troisième classe particulière empêchée perpétuellement 
        elif not date - paques >= datetime.timedelta(-46) and not date - paques < datetime.timedelta(0) and not objet.DateCivile(paques,annee) < datetime.date(annee,12,25) and not objet.DateCivile(paques,annee) >= premier_dimanche_avent:
            if objet.priorite <= 700 and objet.priorite >= 550 and objet.priorite < adversaire.priorite and not objet.dimanche:
                objet.date = objet.date + datetime.timedelta(1)
                Annee=traite(Annee,objet, date + datetime.timedelta(1),annee)
            elif adversaire.priorite <=700 and objet.priorite >= 550 and objet.priorite > adversaire.priorite and not adversaire.dimanche:
                Annee[date][0] = objet
                adversaire.date = adversaire.date + datetime.timedelta(1)
                Annee=traite(Annee,adversaire,date + datetime.timedelta(1),annee)
    else:
        Annee[date].append(objet)
    Annee[date].sort(key=lambda x: x.priorite,reverse=True)
    return Annee
    
def selection(liste,date,Annee,samedi):
    """Selects the feasts which are actually celebrated."""
    commemoraison = 0 # max 2
    commemoraison_temporal=False
    
    if samedi.Est_ce_samedi(date):
        samedi.date = date
        liste.append(samedi)
    else:
        try:
            ferie = FeteFerie()
            if liste[0].degre == 5:
                ferie.Dimanche_precedent(date,Annee)
                liste.append(ferie)
        except IndexError:
            ferie.Dimanche_precedent(date,Annee)
            liste.append(ferie)
    liste.sort(key=lambda x: x.priorite,reverse=True)
    
    liste[0].commemoraison = False
    liste[0].omission = False
    liste[0].celebree=True
    i="nothing, it's just for the joke. How funny I am !"
    tmp = liste[0]
    liste = sorted(liste[1:], key=lambda a: a.commemoraison_privilegiee, reverse=True)
    
    if tmp.dimanche or tmp.fete_du_Seigneur and datetime.date.isoweekday(date) == 7:
        for hideux, elt in enumerate(liste):
            liste[hideux].omission = True
            liste[hideux].celebree = False
    elif tmp.degre == 1:
        for hideux,elt in enumerate(liste):
            liste[hideux].celebree=False
            if elt.personne == tmp.personne:
                liste[hideux].omission = True
                liste[hideux].celebree = False
            elif elt.commemoraison_privilegiee > 0 and commemoraison == 0 and not (tmp.fete_du_Seigneur and elt.dimanche or tmp.dimanche and elt.fete_du_Seigneur):
                liste[hideux].commemoraison=True
                commemoraison = 1
            else:
                liste[hideux].commemoraison=False
                liste[hideux].omission=True
                
    elif tmp.degre == 2:
        for hideux,elt in enumerate(liste):
            liste[hideux].celebree=False
            if elt.personne == tmp.personne:
                liste[hideux].omission = True
                liste[hideux].celebree = False
            elif commemoraison == 0 and elt.degre <= 2 and not (tmp.fete_du_Seigneur and elt.dimanche or tmp.dimanche and elt.fete_du_Seigneur):
                liste[hideux].commemoraison=True
                commemoraison = 1
            else:
                liste[hideux].commemoraison=False
                liste[hideux].omission=True
                
    elif tmp.degre == 3:
        for hideux,elt in enumerate(liste):
            liste[hideux].celebree=False
            if elt.personne == tmp.personne:
                liste[hideux].omission = True
                liste[hideux].celebree = False
            elif commemoraison <= 2 and not commemoraison_temporal:
                liste[hideux].commemoraison=True
                commemoraison_temporal=liste[hideux].temporal
                commemoraison += 1
            else:
                liste[hideux].commemoraison=False
                liste[hideux].omission=True
    
    elif tmp.degre == 4:
        tmp.celebree=False
        tmp.peut_etre_celebree=True
        for hideux,elt in enumerate(liste):
            liste[hideux].celebree=False
            liste[hideux].peut_etre_celebree=True
            if elt.personne == tmp.personne:
                liste[hideux].omission = True
            elif commemoraison <= 2 and not commemoraison_temporal:
                liste[hideux].commemoraison=True
                commemoraison_temporal=liste[hideux].temporal
                commemoraison += 1
            else:
                liste[hideux].commemoraison=False
                liste[hideux].omission=True
    
    liste = [tmp] + liste
    liste.sort(key=lambda x: x.priorite,reverse=True)
    
    return liste

def affiche_temps_liturgique(objet,langue='francais'):
    """Une fonction capable d'afficher le temps liturgique"""
    sortie = 'erreur'
    if langue == 'francais':
        if objet.temps_liturgique == 'nativite':
            sortie = "temps de la Nativité (Temps de Noël)"
        elif objet.temps_liturgique == 'epiphanie':
            sortie = "temps de l'Épiphanie (Temps de Noël)"
        elif objet.temps_liturgique == 'avent':
            sortie = "temps de l'Avent"
        elif objet.temps_liturgique == 'apres_epiphanie':
            sortie = "temps per Annum après l'Épiphanie"
        elif objet.temps_liturgique == 'septuagesime':
            sortie = "temps de la Septuagésime"
        elif objet.temps_liturgique == 'careme':
            sortie = "temps du Carême proprement dit (Temps du Carême)"
        elif objet.temps_liturgique == 'passion':
            sortie = "temps de la Passion (Temps du Carême)"
        elif objet.temps_liturgique == 'paques':
            sortie = "temps de Pâques (Temps Pascal)"
        elif objet.temps_liturgique == 'ascension':
            sortie = "temps de l'Ascension (Temps Pascal)"
        elif objet.temps_liturgique == 'octave_pentecote':
            sortie = "octave de la Pentecôte (Temps Pascal)"
        elif objet.temps_liturgique == 'pentecote':
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
        mois = mois_lettre(date.month - 1,langue)
        sortie="""le {} {} {}""".format(jour,mois,date.year)
    elif kwargs['langue']=='english':
        sortie="""on {}""".format(date)
    elif kwargs['langue']=='latina':
        sortie="""in {}""".format(date) # à développer
    
    return sortie

def affichage(**kwargs):
    """Une fonction destinée à l'affichage des résultats."""
    if kwargs['verbose'] and not kwargs['recherche']:
        sortie = affiche_jour(kwargs['date'],kwargs['langue']).capitalize() + ', '
    else:
        sortie=''
        
    for a in kwargs['liste']:
        if a.omission and not kwargs['verbose'] and not kwargs['recherche']:
            continue
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
                    
                premier_mot = a.nom['francais'].split()[0].lower() # peut-être traiter aussi le deuxième mot ; avec une regex ?
                if [True for i in ('dimanche',) if i in premier_mot]:
                    sortie += 'le '
                elif [True for i in ('dédicace','présentation') if i in premier_mot]:
                    sortie += 'la '
                elif [True for i in ('saints',) if i in premier_mot]:
                    sortie += 'les '
                elif [True for i in ('office','octave',) if i in premier_mot]:
                    sortie += "l'"
            
            if kwargs['date_affichee'] and not kwargs['verbose'] and not kwargs['recherche']:
                sortie += """{}/{}/{} : """.format(kwargs['date'].day,kwargs['date'].month,kwargs['date'].year)
            sortie += a.nom['francais']
            
            if not kwargs['verbose'] and a.commemoraison:
                sortie += ' (Commémoraison)'
            elif not kwargs['verbose'] and kwargs['recherche'] and a.omission:
                sortie += ' (omis)'
                
            if kwargs['recherche'] and kwargs['verbose']:
                sortie += ' ' + affiche_jour(a.date,kwargs['langue']) #rajouter le jour de la semaine
                
            if kwargs['recherche'] and not kwargs['verbose']:
                sortie += """ : {}/{}/{}""".format(a.date.day,a.date.month,a.date.year)
                
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
                    origine = a.DateCivile_(paques,kwargs['date'].year)
                    if origine.day == 1:
                        jour = 'premier'
                    else:
                        jour = kwargs['date'].day
                    mois = mois_lettre(kwargs['date'].month - 1,kwargs['langue'])
                    sortie += """Fête transférée du {} {} {}. """.format(jour, mois, origine.year)
                  
            if kwargs['verbose'] or kwargs['temporal_ou_sanctoral']:
                if a.temporal:
                    sortie += """Fête du Temps. """
                else:
                    sortie += """Fête du Sanctoral. """
                    
            if kwargs['verbose'] or kwargs['temps_liturgique']: # ne peut marcher qu'avec une année complète supprimer False une fois que c'est corrigé ; ne peut être un simple affichage : ce qui sera enregistré le sera sous une forme plus sobre.
                sortie += """Temps liturgique : {}. """.format(affiche_temps_liturgique(a,'francais').capitalize())
                
            if kwargs['verbose'] or kwargs['couleur']:
                sortie += """Couleur liturgique : {}. """.format(a.couleur)
            
            if kwargs['verbose']:
                sortie += a.addendum[kwargs['langue']]
                
        elif kwargs['langue'] == 'english':
            erreur('01')
        else: # latin
            pass
        sortie += '\n'
            
    return sortie
            

def ouvreetregarde(fichier,Annee,ordo,propre,annee,paques):
    """Open the file 'fichier', and load the objects in it. If objet.ordo with 'ordo' and 'propre' with objet.propre, add the objet to a dict 'Annee', which is an emulation of the year 'Annee', with the key returned by objet.DateCivile."""
    with open(fichier, 'rb') as file:
        pic=pickle.Unpickler(file)
        boucle=True
        while boucle:
            try:
                objet=pic.load()
                if ordo == objet.ordo and trouve(propre,objet.propre,latinus):
                    if isinstance(objet.DateCivile(paques,annee),datetime.date):
                        date=objet.DateCivile(paques,annee)
                        Annee = traite(Annee,objet,date,annee,propre)
                    else:
                        for a in objet.DateCivile(paques,annee):
                            Annee = traite(Annee,a,objet.DateCivile(paques,annee),annee,propre)
            except EOFError:
                boucle=False
    return Annee
                    

def remonte(liste, entre, nom='latinus'):
    """Function used in the 'trouve' function. Find the proper which is before the 'entre' one in the 'liste'."""
    if entre in liste.keys():
        entre=nom
        return nom
    for a in liste.keys():
        entre=remonte(liste[a],entre,a)
    return entre

def trouve(entre,cherche,liste=latinus):
    """Returns a boolean. Find if the propre 'entre' matches whith the propre 'cherche' in the 'liste'."""
    if entre == cherche:
        return True
    else:
        sortie=entre
        while sortie != 'latinus':
            sortie=remonte(liste, sortie)
            if sortie == cherche:
                return True
    return False

def paques(an):
    """Return a datetime.date object with the Easter date of the year 'an'. The function is only available between 1583 and 4100.
    I didn't write this function, but I found it here : http://python.jpvweb.com/mesrecettespython/doku.php?id=date_de_paques """
    a=an//100
    b=an%100
    c=(3*(a+25))//4
    d=(3*(a+25))%4
    e=(8*(a+11))//25
    f=(5*a+b)%19
    g=(19*f+c-e)%30
    h=(f+11*g)//319
    j=(60*(5-d)+b)//4
    k=(60*(5-d)+b)%4
    m=(2*j-k-g+h)%7
    n=(g-h+m+114)//31
    p=(g-h+m+114)%31
    jour=p+1
    mois=n
    return datetime.date(an,mois,jour)

def dimancheavant(jour):
    """Une fonction qui renvoie le dimanche d'avant le jour concerné. jour doit être un datetime.date."""
    return jour - datetime.timedelta(datetime.date.isoweekday(jour))
    
def dimancheapres(jour):
    """Une fonction qui renvoie le dimanche d'après le jour concerné. jour doit être un datetime.date."""
    ecart=datetime.timedelta(7 - datetime.date.isoweekday(jour))
    return jour + ecart if ecart.days != 0 else jour + datetime.timedelta(7)
    

    
# classes
class Textes:
    """Classe conteneur des textes de la messe et des Vêpres. Encore en chantier."""
    def __init__(self):
        self.contenu='un contenu pour ne pas faire planter les sauvegardes xml'


class Fete:
    """Classe mère de toutes les classes de fêtes.""" 
    def __init__(self,festivitas=''):
        """Liste des attributs"""
        self.nom={'latina':festivitas,'francais':str(),'english':str()} # le nom dans diverses langues
        
        self.degre=int() # entre 1 et 5, 5 représentant une mémoire
        self._priorite=int()
        self.commemoraison_privilegiee=int()
        
        self.propre='romanus' # a string with the propre the feast belongs to 
        self.ordo=1962 # Default : 1962 ordo. The others may be : 1955,1942,1914
        self._couleur='vert' # vert par défaut 
        self.date_='' # un élément qui permet de calculer la date

        self.personne='deuxieme' # indique quel saint ou personne divine est célébrée. Très important pour le classement.
        self.fete_du_Seigneur=False
        
        self.occurrence_perpetuelle=False # Pour toutes les fêtes souffrant d'une occurrence perpetuelle avec une autre fête.
        self.dimanche=False # Pour les dimanches
        self.repris_en_ferie=False # Pour les jours qui sont repris en férie
        
        self.temporal=False
        self.sanctoral=False
        self._temps_liturgique = 'variable' # un élément qui permet de connaître le temps liturgique
        
        self.link=str() # un lien vers Introibo, en attendant une classe spéciale textes.
        self.textes='' # Textes de la messe et des Vêpres, pour plus tard
        self.addendum={'francais':'',
                       'english':'',
                       'latina':'',
                       } # à ajouter à l'affichage. Par exemple, fête de la dédicace : priorité uniquement pour l'église en question.

        self.pal=False # pal=Pro aliquibus locis
        self.votive=False # Si la messe est votive, ou peut être reprise comme votive.
        
        #Éléments variables selon l'année
        self.peut_etre_celebree=False
        self.transferee=False
        self.date=None # la date effective
        self.celebree=True
        self.omission=False # paramètre qui peut changer en fonction des dates
        self.commemoraison=False # paramètre qui peut changer en fonction des dates
        # RegEx
        self.regex_={'nom_compose':[],
                    'attribut_compose':[],
                    'hyperonyme':[],
                    'syntaxiques':[],
                    'titre':[],
                    'attribut':[],
                    'nom':[],
                    'egal':[], # à utiliser : deuxième dimanche de la passion, par exemple.
                    'refus_fort':[],
                    'refus_faible':[],                    
            } # les éléments propres de la regex, avant compilation
        self.regex=None# la regex véritable, après compilation avec la fonction à créer

    # Définitions de certaines méthodes spéciales
    def __str__(self):
        """Méthode affichant des informations sur l'objet grâce à print"""
        return """{}, fête de {} classe selon le missel de {}.""".format(self.nom['latina'],self.degre,self.ordo)
    def __repr__(self):
        """Méthode affichant le nom de l'objet"""
        return self.nom['latina']
    def __lt__(self,autrefete):
        """Méthode pour comparer les objets ensemble, et surtout pour les trier dans la liste (via un list.sort(). ordo représente la variable globale utilisée dans le reste du script.)""" # Je crains que cette fonction ne serve à rien.
        if self.degre == autrefete.degre:
            return self.priorite < autrefete.priorite
        else:
            return self.degre < autrefete.degre
    def __eq__(self,autrefete):
        """Méthode pour comparer deux objets type Fete"""
        if isinstance(autrefete,Fete):
            return self.__dict__ == autrefete.__dict__
        else:
            raise TypeError("""{} is not a 'Fete' class, or any of her subclasses.""".format(autrefete))
        
    # Définitions de méthodes   
    def Votive(self):
        """Une fonction calculant quels jours on peut célébrer la messe votive. Que renvoie-t-elle ?"""
        pass
    
    def DateCivile_(self,paques,annee):
        pass
    
    def DateCivile(self,paques,annee):
        """Une fonction qui va tester si la date est déjà déterminée, sinon il va la demander à la fonction DateCivile_()"""
        if not isinstance(self.date,datetime.date):
            self.date = self.DateCivile_(paques,annee)
        return self.date
    
    def DatePaques(self,paques,annee):
        """Une fonction qui calcule le nombre de jours par rapport à Pâques"""
        return paques - self.DateCivile(paques,annee)
    
    def Correspondance(self,mots,mots_separes):
        """Fonction qui renvoie un chiffre de correspondance entre les mots rentrés et les regex"""
        niveau = 0
        if isinstance(self,FeteFerie):
            return niveau
        for index in self.regex:
            if 'compose' in index:
                i=0
                while i + 1 < len(self.regex[index]):
                    if self.regex[index][i].findall(mots):
                        if self.regex[index][i+1].findall(mots):
                            niveau += 50
                            i += 1
                        else:
                            niveau += 30
                    i+= 1
                continue
            elif index == 'refus_faible':
                for a in self.regex[index]:
                    for mot in mots_separes:
                        if a.fullmatch(mot):
                            niveau -= 8 # 8 normalement
                    
            for a in self.regex[index]:
                if index == 'hyperonyme' and a.fullmatch(mots):
                    niveau += 60
                elif a.findall(mots):
                    if index == 'syntaxiques':
                        niveau += 3
                    elif index == 'titre':
                        niveau += 15
                    elif index == 'attribut':
                        if a.fullmatch(mots):
                            niveau += 46
                        else:
                            niveau += 35
                    elif index == 'nom' or index == 'hyperonyme':
                        niveau += 45
                    elif index == 'egal':
                        niveau += 76/len(self.regex[index])
                    elif index == 'refus_fort':
                        niveau -= 15 # 15 normalement
                    elif index == 'annexes':
                        niveau + 20
                
                for mot in mots_separes: # cela pose problème pour certaines regex, qui sont composées de deux mots. (in albis par exemple)
                    if a.fullmatch(mot):
                        if 'refus' in index:
                            niveau -= 5 #5 normalement
                        else:
                            niveau += 10
            
        
        return niveau
    
    def Correspondance2(self,liste,attache): # ceci n'est qu'un modèle à améliorer ; l'incrémentation fonctionne.
        """Une fonction permettant de rechercher les mots d'une autre manière."""
        liste_match=[]
        for mot in liste:
            compteur = 0
            hideux = 0
            for i, lettre in enumerate(mot):
                nouveau = mot
                if lettre == '(':
                    compteur += 1
                    if compteur == 1:
                        hideux = i
                    continue
                if lettre == ')':
                    compteur -= 1
                if compteur == 0:
                    print(i,hideux)
                    nouveau = mot[:hideux] + '.?' + mot[i+1:]
                    print(nouveau)
                    hideux = i+1
                    if re.search(nouveau,attache):
                        liste_match.append(mot)
                        break
        return liste_match
    
    # Définitions de propriétés
    def _get_priorite(self):
        """Une fonction pour renvoyer self._priorite."""
        return self._priorite
    
    priorite = property(_get_priorite)
    
    def _get_temps_liturgique(self):
        """Une fonction qui renvoie le temps liturgique"""
        if self._temps_liturgique == 'variable':
            date = self.date
            from __main__ import Annee
            while True:
                try:
                    for a in Annee[date]:
                        if a.temporal:
                            return a.temps_liturgique
                    date = date - datetime.timedelta(1)
                except KeyError:
                    continue
        else:
            return self._temps_liturgique
    
    temps_liturgique = property(_get_temps_liturgique)
    
    def _get_couleur(self):
        """Une fonction qui calcule la couleur des ornements"""
        return self._couleur
    
    couleur = property(_get_couleur)
    
class FeteFixe(Fete):
    """Une classe définissant une fête fixe, c'est-à-dire dont la date ne change pas dans l'année."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_={
            'mois':int(),
            'jour':int(),
            }           
    
    def DateCivile_(self,paques,annee):
        """Renvoie la date de l'année civile."""
        return datetime.date(annee,self.date_['mois'],self.date_['jour'])
        
class FeteFixeBissextile(Fete):
    """Une classe définissant une fête fixe qui change lors des années bissextiles."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_={
            'bissextile': {
                'mois':int(),
                'jour':int(),
                },
            'ordinaire': {
                'mois':int(),
                'jour':int(),
                },
            }
            
    def DateCivile_(self,paques,annee):
        """Renvoie la date de l'année civile."""
        if calendar.isleap(annee):
            return datetime.date(annee,self.date_['bissextile']['mois'],self.date_['bissextile']['jour'])
        else:
            return datetime.date(annee,self.date_['ordinaire']['mois'],self.date_['ordinaire']['jour'])
        
class FeteMobilePaques(Fete):
    """Une classe définissant une fête mobile, par rapport à Pâques."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_=int() # ne comprend qu'un entier correspondant au nombre de jours par rapport à Pâques
    
    def DateCivile_(self,paques,annee):
        """Calcule la date civile d'une fête mobile."""
        return paques + datetime.timedelta(self.date_)
    
class FeteMobileDerniersDimanchesPentecote(Fete):
    """Une classe définissant les derniers dimanches après la Pentecôte, à partir du 23 ème."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_={} # un dictionnaire prenant pour clef le nombre de jours entre Pâques et le quatrième dimanche de l'Avent, et en valeur le nombre de jours entre Pâques et le jour de la fête.
    
    def DateCivile_(self,paques,annee):
        """Calcule la date par rapport à Pâques et Noël."""
        ecart = dimancheavant(datetime.date(annee,12,25)) - paques
        try:
            return paques + datetime.timedelta(self.date_[ecart.days])
        except KeyError:
            self._priorite = 0
            return paques + ecart - datetime.timedelta(28) # renvoie au dernier dimanche après la Pentecôte.
    
class FeteMobileAvent(Fete):
    """Une classe définissant les fêtes de l'Avent. On pourrait les faire basculer dans les derniers dimanches après la Pentecôte."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_=int() # Un entier correspondant au nombre de jours par rapport au quatrième dimanche de l'Avent.
        
    def DateCivile_(self,paques,annee):
        """Calcule la date civile en fonction du nombre de jours d'écart avec le quatrième dimanche de l'Avent."""
        retour= dimancheavant(datetime.date(annee,12,25)) - datetime.timedelta(self.date_)
        if retour > datetime.date(annee,12,24):
            retour = datetime.date(annee,12,24)
            self._priorite = 0
            self.commemoraison_privilegiee = -1
        return retour 

class FeteMobileEpiphanie(Fete):
    """Une classe définissant une fête mobile dépendant de l'Epiphanie."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_=int() # Un entier correspondant au nombre de jours après le premier dimanche après l'Epiphanie
    
    def DateCivile_(self,paques,annee):
        """Calcule la date par rapport à Pâques et au premier dimanche après l'Epiphanie."""
        septuagesime = paques - datetime.timedelta(63)
        retour= dimancheapres(datetime.date(annee,1,6)) + datetime.timedelta(self.date_)
        if retour > septuagesime:
            retour = septuagesime
            self._priorite = 0
            self.commemoraison_privilegiee = -1
        return retour
    
    def _get_couleur(self):
        if self.date >= datetime.date(self.date.year,1,14):
            return 'vert'
        else:
            return self._couleur
        
    couleur = property(_get_couleur)

class FeteMobileMois(Fete):
    """Une classe définissant une fête qui se calcule en fonction de sa place dans un mois particulier.
    self.date contient un dictionnaire à trois entrées : le numéro de mois, le jour de la semaine(0=lundi), et un chiffre représentant son ordre d'apparition dans le mois (0 représente la première semaine, -1 représente le dernier)
    Exemple: { 'mois' : 10, 'jour': 6, 'ordre': 0} = premier dimanche du mois d'octobre."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_={
            'mois' : 1,
            'jour' : 0,
            'ordre' : -1,
            }
        
    def DateCivile_(self,paques,annee):
        """Calcule la date civile."""
        jouran = calendar.monthcalendar(annee,self.date_['mois'])[self.date_['ordre']][self.date_['jour']]
        
        if jouran == 0 and self.date_['ordre'] > -1:
            jouran = calendar.monthcalendar(annee,self.date_['mois'])[self.date_['ordre'] + 1][self.date_['jour']]
        elif jouran == 0 and self.date_['ordre'] < 0:
            jouran = calendar.monthcalendar(annee,self.date_['mois'])[self.date_['ordre'] - 1][self.date_['jour']]
            
        return datetime.date(annee,self.date_['mois'],jouran)
    
class FeteFixeTransferablePaques(FeteFixe):
    """Une classe pour toutes les fêtes fixes qui peuvent être transférées et dont la date se calculera par rapport à Pâques.""" #Pour l'Annonciation et les litanies majeures
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.borne_debut=int()
        self.borne_fin=int()
        self.transfert=int()
    
    def DateCivile_(self,paques,annee):
        """Une fonction calculant la date civile."""
        datedebase=datetime.date(annee,self.date_['mois'],self.date_['jour'])
        if datedebase < paques + datetime.timedelta(self.borne_debut) or datebase > paques + datetime.timedelta(self.borne_fin):
            return datebase
        else:
            return paques + datetime.timedelta(self.transfert)
        
class FeteFixeTransferableDimanche(FeteFixe):
    """Une classe pour toutes les fêtes fixes qui peuvent être transférées et dont la date sera un dimanche."""
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.ecart_dimanche=int() # combien de dimanches d'écart
        self.apres=True # indique s'il faut voir le dimanche d'avant ou d'après
        
    def DateCivile_(self,paques,annee):
        """Une fonction calculant la date civile."""
        if self.apres:
            return datetime.date(dimancheapres(self.date_) + datetime.timedelta(self.ecart_dimanche*7))
        else:
            return datetime.date(dimancheavant(self.date_) - datetime.timedelta(self.ecart_dimanche*7))
        
class FeteFerie(Fete):
    """Une classe définissant des jours de férie, comprenant une liste de dates en dehors des fêtes fixes.""" # les dates à rentrer ne sont pas très utiles. Il suffirait de vérifier qu'il n'y ait rien, au jour demandé, d'autre que des commémoraisons...
    
    def __init__(self):
        Fete.__init__(self)
        self.degre=4
        self._priorite=200
        self.commemoraison_privilegiee=-1
    
    def QuelNom(self,jour):
        """Une fonction qui renvoie le nom qui doit être donné au jour de férie."""
        i = datetime.date.weekday(jour)
        nomen = ['secunda','tertia','quarta','quinta','sexta']
        nom = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi']
        name = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        return {'latina':'Feria ' + nomen[i],
                'francais':nom[i] + ' de la férie du ' + affiche_temps_liturgique(self,'francais'),
                'english':name[i]} # Comment dit on jour de férie en anglais ?
    
    def Dimanche_precedent(self,jour,Annee):
        """Une fonction qui renvoie le dimanche précédent, si la férie est attestée, et change son nom, sa classe, priorite, et commemoraison_privilegiee.""" # changer cette aide
        curseur = jour
        boucle = True
        while boucle:
            curseur = curseur - datetime.timedelta(1)
            try:
                for office in Annee[curseur]:
                    if office.repris_en_ferie:
                        self.date=jour
                        self.propre = office.propre
                        self.link = office.link
                        self.addendum = office.addendum
                        if jour >= datetime.date(jour.year,1,14) and office.temps_liturgique == 'epiphanie':
                            self._temps_liturgique = 'apres_epiphanie'
                            self._couleur = 'vert'
                        else:
                            self._temps_liturgique = office._temps_liturgique
                            self._couleur = office.couleur
                        self.nom = self.QuelNom(jour)
                        boucle = False
                        break
            except KeyError:
                continue
        
class Samedi(Fete):
    """Une fête définissant l'office de la sainte Vierge du samedi"""
    
    def Est_ce_samedi(self,jour):
        """Une fonction qui renvoie un booléen si le jour considéré est un samedi"""
        return True if datetime.date.isoweekday(jour) == 6 else False
    
#classe de fêtes sui generis
class TSNJ(FeteFixe):
    """Une classe définissant la fête du Très Saint Nom de Jésus, et toutes celles qui lui ressemblent."""
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.limite_basse=2
        self.limite_haute=5 # les limites correspondent à des jours pendant lesquels la fête est susceptible de tomber
        
    def DateCivile_(self,paques,annee):
        """Une fonction qui détermine la date pour une année précise."""
        dimanche=calendar.monthcalendar(annee,self.date_['mois'])[0][6]
        if dimanche <= self.limite_haute and dimanche >= self.limite_basse:
            self.dimanche=True
            return datetime.date(annee,self.date_['mois'],dimanche)
        else:
            self.dimanche=False
            return datetime.date(annee,self.date_['mois'],self.date_['jour'])

class Defunts(FeteFixe):
    """Une classe pour la commémoraison des fidèles défunts."""
    
    def __init__(self):
        FeteFixe.__init__(self)
        
    def _get_priorite(self):
        """Détermine quelle sera la valeur de la priorité selon que le jour sera un dimanche ou non."""
        if datetime.date.isoweekday(self.date) != 7:
            return 2100
        else:
            return 1499 # càd juste en-dessous d'un dimanche de deuxième classe
        
    priorite=property(_get_priorite)
    
class DimancheOctaveNoel(Fete):
    """Une classe définisssant les fêtes mobiles après Noël."""
    
    def __init__(self):
        Fete.__init__(self)
        
    def DateCivile_(self,paques,annee):
        """Calcule la date civile en fonction du premier dimanche après Noël."""
        if dimancheapres(datetime.date(annee,12,25)) == datetime.date(annee + 1,1,1):
            self._priorite = 0
        return dimancheapres(datetime.date(annee,12,25))
    
# classes de fêtes à plusieurs dates

class JoursOctaveDeNoel(FeteFixe): # Pour le moment, impossible de les rechercher sans discriminer entre eux
    """Une classe pour les jours dans l'Octave de Noël"""
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.nom_={'francais':"jour dans l'Octave de Noël",'latina':'Die infra octavam Nativitatis','english':'day in the Octave of Christmas'} 
        self.compléments_nom={'francais':['Deuxième','Troisième','Quatrième','Cinquième','Sixième','Septième'],
                              'latina': ['De Secunda','De Tertia','De Quarta','De Quinqua', 'De Sexta','De Septima'],
                              'english': ['Secund','Third','Fourth','Fifth','Sixth','Seventh',]
                              }
        self.date_=[26,27,28,29,30,31]
        self.mois_ = 12
        
    def DateCivile(self,paques,annee):
        """Renvoie une liste de dates"""
        for i,a in enumerate(self.date_):
            retour = FeteFixe()
            retour.__dict__ = copy.deepcopy(self.__dict__)
            for hideux, a in self.regex['refus_fort']:
                if a.match(str(i+2)):
                    self.regex['egal'].append(a)
                    del(self.regex['refus_fort'][hideux])            
            for langue in ('francais','latina','english'):
                retour.nom[langue] = self.compléments_nom[langue][i] + ' ' + self.nom_[langue]
            retour.date = datetime.date(annee,self.mois_,self.date_[i])
            yield retour
            
class JoursAvent(FeteMobileAvent):
    """Une classe pour les jours de férie de l'Avent"""
    pass

    

