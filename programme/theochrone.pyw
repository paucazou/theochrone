#!/usr/bin/env python3.5
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
#chemin = os.path.dirname(os.path.abspath(__file__))
#os.chdir(chemin)

from command_line import AutoCompleter

autocomplete = AutoCompleter()
autocomplete.autocomplete()

import annus
import calendar
import datetime
import martyrology
import officia
import phlog
import shiptobrowser
import subprocess
import sys
import webbrowser
from messages import args

logger = phlog.loggers['console']
logger.debug(args)

def main():
    """main function"""
### Traitement des informations entrées par l'utilisateur ###
    if args.settings != None:
        if args.settings.lower() == "off":
            officia.pdata(SET='OFF')
        elif args.settings.lower() == "on":
            officia.pdata(SET='ON')
        else:
            try:
                int(args.settings)
                officia.pdata(max_history=args.settings)
                args.settings = "History maximum lines number : {}".format(args.settings)
            except ValueError:
                officia.pdata(langue=args.langue)
                args.settings = "Default language : {}".format(args.langue)
            
        sys.exit("Settings saved : {}".format(args.settings))
            

    if args.poems:
        webbrowser.open_new_tab("http://philippeaucazou.wordpress.com")
        sys.exit()
        
    if args.historique:
        if not officia.pdata():
            pass
        elif args.INVERSE != 1:
            history = officia.pdata(history='reverse')
            taille = len(history)
            for i,line in enumerate(history):
                i = taille - i
                print("{} - {} : {}/{} : {}".format(i,line[0].strftime(_('%Y-%m-%d-%HH%M')),line[1].year,line[2].year,' '.join(line[3])))
        else:
            history = officia.pdata(history='dates')
            taille = len(history)
            for i,line in enumerate(history):
                i = taille - i
                print("{} - {} : {} : {}/{}".format(i,line[0].strftime(_('%Y-%m-%d-%HH%M')),line[1],line[2][0],line[2][1]))
        sys.exit()
            
    semaine_seule = mois_seul = annee_seule = fromto = False

    if args.precedent or args.suivant: # do not forget day !!!
        if not args.entree_historique:
            i = 1
        else:
            i = args.entree_historique
        try:
            entree = officia.pdata(history='dates')[-i]
        except (IndexError, TypeError):
            officia.erreur(32,args.langue)
        if args.suivant:
            i = args.suivant
            if entree[1] == 'day':
                debut = fin = entree[2][0] + datetime.timedelta(1*i)
            elif entree[1] == 'week':
                semaine_seule = True
                fin = entree[2][1] + datetime.timedelta(7*i)
                debut= fin - datetime.timedelta(6)
            elif entree[1] == 'month':
                month = entree[2][0].month + 1*i
                debut = datetime.date(entree[2][0].year + int(month/12),month%12,1)
                fin = datetime.date(debut.year,debut.month,debut.day - 1 + calendar.monthrange(debut.year,debut.month)[1])
                mois_seul = True
            elif entree[1] == 'year':
                debut, fin = datetime.date(entree[2][0].year + 1*i,1,1), datetime.date(entree[2][0].year + 1*i,12,31)
                annee_seule = True
            elif entree[1] == 'arbitrary':
                fromto=True
                ecart = entree[2][1] - entree[2][0]
                fin = entree[2][1] + (ecart + datetime.timedelta(1))*i
                debut = fin - ecart
        else:
            i = args.precedent
            if entree[1] == 'day':
                debut = fin = entree[2][0] - datetime.timedelta(1*i)
            elif entree[1] == 'week':
                semaine_seule = True
                fin = entree[2][1] + datetime.timedelta(-7*i)
                debut= fin - datetime.timedelta(6)
            elif entree[1] == 'month':
                month = entree[2][0].month - 1*i
                debut = datetime.date(entree[2][0].year + -int(month/12),month%12,1)
                fin = datetime.date(debut.year,debut.month,debut.day - 1 + calendar.monthrange(debut.year,debut.month)[1])
                mois_seul = True
            elif entree[1] == 'year':
                debut, fin = datetime.date(entree[2][0].year - 1*i,1,1), datetime.date(entree[2][0].year - 1*i,12,31)
                annee_seule = True
            elif entree[1] == 'arbitrary':
                fromto=True
                ecart = entree[2][1] - entree[2][0]
                fin = entree[2][1] - (ecart + datetime.timedelta(1))*i
                debut = fin - ecart

    elif args.entree_historique:
        if args.INVERSE == 1:
            try:
                entree = officia.pdata(history='dates')[-args.entree_historique]
            except IndexError:
                officia.erreur(32,args.langue)
            if entree[1] == 'week':
                semaine_seule = True
            elif entree[1] == 'month':
                mois_seul = True
            elif entree[1] == 'year':
                annee_seule = True
            debut,fin = entree[2]
        else:
            try:
                entree = officia.pdata(history='reverse')[-args.entree_historique]
            except IndexError:
                officia.erreur(32,args.langue)
            debut, fin = entree[1], entree[2]
            args.INVERSE = entree[3]
        
    elif args.DEPUIS == 1 and args.JUSQUE == 1 or args.TODAY:
        date, semaine_seule, mois_seul, annee_seule = officia.datevalable(args.DATE,args.langue)
        debut, fin = officia.AtoZ(semaine_seule,mois_seul,annee_seule,date)
    else:
        fromto=True
        aujourdhui = datetime.date.today()
        if args.DEPUIS != 1:
            args.DEPUIS, semaine_seule, mois_seul, annee_seule = officia.datevalable(args.DEPUIS,args.langue)
            if args.JUSQUE == 1 and args.DEPUIS <= aujourdhui: # WARNING name aujourdhui is not defined WARNING BUG
                fin = aujourdhui
            elif args.JUSQUE == 1:
                fin = datetime.date(args.DEPUIS.year,12,31)
            debut = officia.AtoZ(semaine_seule,mois_seul,annee_seule,args.DEPUIS)[0]
                
        if args.JUSQUE != 1 and not isinstance(args.JUSQUE,datetime.date):
            args.JUSQUE, semaine_seule, mois_seul, annee_seule = officia.datevalable(args.JUSQUE,args.langue)
            if args.DEPUIS == 1 and args.JUSQUE >= aujourdhui:
                debut = aujourdhui
            elif args.DEPUIS == 1:
                debut = datetime.date(args.JUSQUE.year,1,1)
            fin = officia.AtoZ(semaine_seule,mois_seul,annee_seule,args.JUSQUE)[1]
        
        if fin < debut:
            officia.erreur(16,args.langue)

    if args.INVERSE == 1 and not fromto:
        officia.pdata(write=True,history='dates',debut=debut,fin=fin,
                    semaine_seule=semaine_seule,mois_seul=mois_seul,annee_seule=annee_seule)
    elif fromto:
        officia.pdata(write=True,history='dates',debut=debut,fin=fin,fromto=True)
    elif args.INVERSE != 1:
        officia.pdata(write=True,history='reverse',debut=debut,fin=fin,keywords=args.INVERSE)

    if args.navigateur:
        if mois_seul:
            sys.exit(shiptobrowser.openBrowser(search_type='month',date=debut))
        elif args.INVERSE != 1:
            sys.exit(shiptobrowser.openBrowser(search_type='reverse',date=debut,keywords=args.INVERSE))
        elif not semaine_seule and not mois_seul and not annee_seule and args.DEPUIS == 1 and args.JUSQUE == 1:
            sys.exit(shiptobrowser.openBrowser(search_type='day',date=debut))
        else:
            sys.exit(shiptobrowser.openBrowser())
    elif not os.isatty(0) or args.gui or (len(sys.argv) <= 1 and not sys.platform.startswith('linux')):
        from gui import main_window
        app = main_window.App([args.INVERSE,debut,fin,args.plus])
        sys.exit(app.exec_())
        
### Définition de quelques variables ###  
    ordo=args.ordo

### Analyse des fichiers ###
    #Annee = officia.fabrique_an(debut,fin,ordo,argsr.propre)
    Annee = annus.LiturgicalCalendar(args.propre,ordo)
    Annee(debut.year,fin.year)
    roman_martyrology = martyrology.Martyrology(args.ordo)

#### Affichage ###

    if args.INVERSE != 1: # des raisons aléatoires semblent s'appliquer...
        if args.martyrology:
            results = roman_martyrology.kw(args.INVERSE,args.langue,5) # TODO ajouter le ratio ou le nb max d'items
            for res in results:
                print(res.title)
                if res.matching_line > 0:
                    print(*res.main[:res.matching_line],sep='\n')
                sys.stdout.write("\033[1;31m") # print red
                print(res.main[res.matching_line])
                sys.stdout.write("\033[0;0m") # print white
                if res.matching_line + 1 != len(res.main):
                    print(*res.main[res.matching_line + 1:],sep='\n')
                print(res.last_sentence,'\n')
        else:
            liste = officia.inversons(args.INVERSE,Annee,debut,fin,plus=args.plus,langue=args.langue,exit=True)
            if args.textes and len(liste) < 4:
                for fete in liste:
                    webbrowser.open_new_tab(fete.link)
                    
            print(officia.affichage(date_affichee=args.date_affichee,temps_liturgique=args.temps_liturgique,recherche=True,                   liste=liste,Annee=Annee,langue=args.langue,date=debut,verbose=args.verbose,degre=args.degre,temporal_ou_sanctoral=args.temporal_ou_sanctoral,couleur=args.couleur,transfert=args.transfert,jour_semaine=args.jour_semaine,station=args.station))
    else:
        if args.textes and debut == fin:
            for fete in Annee[debut]:
                webbrowser.open_new_tab(fete.link)
        date = debut
        while True:
            print(officia.affichage(date_affichee=args.date_affichee,temps_liturgique=args.temps_liturgique,recherche=False,                   liste=Annee[date],Annee=Annee,langue=args.langue,date=date,verbose=args.verbose,degre=args.degre,temporal_ou_sanctoral=args.temporal_ou_sanctoral,couleur=args.couleur,transfert=args.transfert,jour_semaine=args.jour_semaine,station=args.station))
            if args.martyrology:
                first_line,text,last_line = roman_martyrology.daytext(date,args.langue)
                print('\n',roman_martyrology.name[args.langue],*text,last_line,sep='\n')
            date = date + datetime.timedelta(1)
            if date <= fin:
                print('')
            elif date > fin:
                break
            
if __name__ == '__main__':
    main()
