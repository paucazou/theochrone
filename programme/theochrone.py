#!/usr/bin/python3
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

from command_line import AutoCompleter

autocomplete = AutoCompleter()
autocomplete.autocomplete()

import calendar
import datetime
import officia
import subprocess
import sys
import webbrowser
from messages import args
### Traitement des informations entrées par l'utilisateur ###
if args.poems:
    webbrowser.open_new_tab("http://philippeaucazou.wordpress.com")
    sys.exit()
    
if args.historique:
    if args.INVERSE != 1:
        history = officia.pdata(history='reverse')
        for line in history:
            print("{} : {}/{} : {}".format(line[0].strftime(_('%Y-%m-%d-%HH%M')),line[1].year,line[2].year,' '.join(line[3])))
    else:
        history = officia.pdata(history='dates')
        for line in history:
            print("{} : {} : {}/{}".format(line[0].strftime(_('%Y-%m-%d-%HH%M')),line[1],line[2][0],line[2][1]))
    sys.exit()
    
    

if args.DEPUIS == 1 and args.JUSQUE == 1:
    date, semaine_seule, mois_seul, annee_seule = officia.datevalable(args.DATE,args.langue)
    debut, fin = officia.AtoZ(semaine_seule,mois_seul,annee_seule,date)
else:
    if args.DEPUIS != 1:
        date, semaine_seule, mois_seul, annee_seule = officia.datevalable(args.DEPUIS,args.langue)
        if args.JUSQUE == 1 and args.DEPUIS <= aujourdhui:
            fin = aujourdhui
        elif args.JUSQUE == 1:
            fin = datetime.date(args.DEPUIS.year,12,31)
        debut = officia.AtoZ(semaine_seule,mois_seul,annee_seule,date)[0]
            
    if args.JUSQUE != 1 and not isinstance(args.JUSQUE,datetime.date):
        date, semaine_seule, mois_seul, annee_seule = officia.datevalable(args.JUSQUE,args.langue)
        if args.DEPUIS == 1 and args.JUSQUE >= aujourdhui:
            debut = aujourdhui
        elif args.DEPUIS == 1:
            debut = datetime.date(args.JUSQUE.year,1,1)
        fin = officia.AtoZ(semaine_seule,mois_seul,annee_seule,date)[1]
    
    if fin < debut:
        officia.erreur(16,args.langue)

if args.INVERSE == 1 and args.DEPUIS == 1 and args.JUSQUE == 1:
    officia.pdata(write=True,history='dates',debut=debut,fin=fin,
                  semaine_seule=semaine_seule,mois_seul=mois_seul,annee_seule=annee_seule)
elif args.INVERSE == 1:
    officia.pdata(write=True,history='date',debut=debut,fin=fin,fromto=True)
elif args.INVERSE != 1:
    officia.pdata(write=True,history='reverse',debut=debut,fin=fin,keywords=args.INVERSE)

if args.navigateur:
    if mois_seul:
        sys.exit(subprocess.run(['./navette_navigateur.py','mois',str(debut.month),str(debut.year)]))
    elif args.INVERSE != 1:
        sys.exit(subprocess.run(['./navette_navigateur.py','inverse',str(debut.year),*args.INVERSE]))
    elif not semaine_seule and not mois_seul and not annee_seule and args.DEPUIS == 1 and args.JUSQUE == 1:
        sys.exit(subprocess.run(['./navette_navigateur.py',str(debut.day),str(debut.month),str(debut.year)]))
    else:
        sys.exit(subprocess.run(['./navette_navigateur.py']))
    
### Définition de quelques variables ###  
ordo=args.ordo

### Analyse des fichiers ###
Annee = officia.fabrique_an(debut,fin,ordo,args.propre)

        
### Affichage ###

if args.INVERSE != 1: # des raisons aléatoires semblent s'appliquer...
    liste = officia.inversons(args.INVERSE,Annee,debut,fin,plus=args.plus,langue=args.langue,exit=True)
    if args.textes and len(liste) < 4:
        for fete in liste:
            webbrowser.open_new_tab(fete.link)
    print(officia.affichage(date_affichee=args.date_affichee,temps_liturgique=args.temps_liturgique,recherche=True,                   liste=liste,langue=args.langue,date=date,verbose=args.verbose,degre=args.degre,temporal_ou_sanctoral=args.temporal_ou_sanctoral,couleur=args.couleur,transfert=args.transfert,jour_semaine=args.jour_semaine))
else:
    if args.textes and debut == fin:
        for fete in Annee[debut]:
            webbrowser.open_new_tab(fete.link)
    date = debut
    while True:
        print(officia.affichage(date_affichee=args.date_affichee,temps_liturgique=args.temps_liturgique,recherche=False,                   liste=Annee[date],langue=args.langue,date=date,verbose=args.verbose,degre=args.degre,temporal_ou_sanctoral=args.temporal_ou_sanctoral,couleur=args.couleur,transfert=args.transfert,jour_semaine=args.jour_semaine))
        date = date + datetime.timedelta(1)
        if date <= fin:
            print('')
        elif date > fin:
            break
