#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende. Domine, ad adjuvandum me festina.

### Sommaire ###
# Arguments #
# Traitement des informations rentrées par l'utilisateur #
# Définition de quelques variables #
# Analyse des fichiers #
# Affichage #
### ###

import os
chemin = os.path.dirname(os.path.abspath(__file__))
os.chdir(chemin)

import adjutoria
from adjutoria import datetime, calendar, pickle, re
from messages import args

### Traitement des informations entrées par l'utilisateur ###
if args.poems:
    adjutoria.ocasu()

if args.INVERSE != 1:
    args.INVERSE = [adjutoria.sans_accent(mot) for mot in args.INVERSE]
    mots = []
    for mot in args.INVERSE:
        if ' ' in mot:
            mots = mots + mot.split()
        else:
            mots = mots + [mot]
    mots = adjutoria.modification(mots,args.langue)
    mots_str=''
    for a in mots:
        mots_str += a

if args.DEPUIS == 1 and args.JUSQUE == 1:
    date, semaine_seule, mois_seul, annee_seule = adjutoria.datevalable(args.DATE,args.langue)
    debut, fin = adjutoria.AtoZ(semaine_seule,mois_seul,annee_seule,date)
else:
    if args.DEPUIS != 1:
        date, semaine_seule, mois_seul, annee_seule = adjutoria.datevalable(args.DEPUIS,args.langue)
        if args.JUSQUE == 1 and args.DEPUIS <= aujourdhui:
            fin = aujourdhui
        elif args.JUSQUE == 1:
            fin = datetime.date(args.DEPUIS.year,12,31)
        debut = adjutoria.AtoZ(semaine_seule,mois_seul,annee_seule,date)[0]
            
    if args.JUSQUE != 1 and not isinstance(args.JUSQUE,datetime.date):
        date, semaine_seule, mois_seul, annee_seule = adjutoria.datevalable(args.JUSQUE,args.langue)
        if args.DEPUIS == 1 and args.JUSQUE >= aujourdhui:
            debut = aujourdhui
        elif args.DEPUIS == 1:
            debut = datetime.date(args.JUSQUE.year,1,1)
        fin = adjutoria.AtoZ(semaine_seule,mois_seul,annee_seule,date)[1]
    
    if fin < debut:
        adjutoria.erreur(16,args.langue)
        
### Définition de quelques variables ###  
Annee = dict()
ordo=args.ordo

### Analyse des fichiers ###
year = debut.year - 1
while True:
    paques = adjutoria.paques(year)
    for fichier in [file for file in adjutoria.fichiers if file.split('_')[1] == str(ordo) and adjutoria.trouve(args.propre,file.split('_')[0])]:
        Annee = adjutoria.ouvreetregarde('./data/' + fichier,Annee,ordo,args.propre,year,paques)
    if year == fin.year:
        break
    else:
        year += 1

with open('./data/samedi.pic','rb') as file:
    pic=pickle.Unpickler(file)
    samedi=pic.load()
    
### Traitement de la recherche inversée ###
if args.INVERSE != 1:
    boucle = True
    date = debut
    if date == fin:
        date = datetime.date(date.year,1,1)
        fin = datetime.date(date.year,12,31)
    retenus = []
    while date <= fin:
        try:
            Annee[date] = adjutoria.selection(Annee[date],date,Annee,samedi)
            for fete in Annee[date]:
                fete.valeur = fete.Correspondance(mots_str,mots)
                if fete.valeur >= 50:
                    retenus.append(fete)
        except KeyError:
            pass
        date += datetime.timedelta(1)
        
### Affichage ###
if args.test and args.verbose:
    for key in Annee:
        print(key)
        for a in Annee[key]:
            print(a)
        print('\n')

if args.INVERSE != 1: # des raisons aléatoires semblent s'appliquer...
    retenus.sort(key=lambda x:x.valeur,reverse=True)
    superieurs = [x for x in retenus if x.valeur >= 70 and x.valeur < 100]
    elite = [x for x in retenus if x.valeur >= 100]
    #print(mots,retenus,superieurs,elite)
    if args.plus:
        liste = retenus
    elif len(elite) >= 1:
        liste = elite
    elif len(superieurs) >= 1:
        liste=superieurs
    elif len(superieurs) == 0 and len(retenus) >= 1:
        liste=retenus
    else:
        adjutoria.erreur(20,args.langue)
    print(adjutoria.affichage(date_affichee=args.date_affichee,temps_liturgique=args.temps_liturgique,recherche=True,                   liste=liste,langue=args.langue,date=date,verbose=args.verbose,degre=args.degre,temporal_ou_sanctoral=args.temporal_ou_sanctoral,couleur=args.couleur,transfert=args.transfert,jour_semaine=args.jour_semaine))
else:
    date = debut
    while True:
        try:
            Annee[date]
        except KeyError:
            Annee[date]=[]
        celebrations = adjutoria.selection(Annee[date],date,Annee,samedi)
        print(adjutoria.affichage(date_affichee=args.date_affichee,temps_liturgique=args.temps_liturgique,recherche=False,                   liste=celebrations,langue=args.langue,date=date,verbose=args.verbose,degre=args.degre,temporal_ou_sanctoral=args.temporal_ou_sanctoral,couleur=args.couleur,transfert=args.transfert,jour_semaine=args.jour_semaine))
        date = date + datetime.timedelta(1)
        if date <= fin:
            print('')
        elif date > fin:
            break
