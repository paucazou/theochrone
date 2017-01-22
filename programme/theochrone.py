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

import adjutoria
from adjutoria import datetime, calendar, argparse, pickle, re

aujourdhui=datetime.date.today()

### Arguments ###
parser = argparse.ArgumentParser(
        prog='Theochrone',
        formatter_class=argparse.RawTextHelpFormatter,
        description="""A universal calendar for the Tridentine Mass (i.e. Extraordinary Form of the Roman Rite)""",
        epilog="Please pray God for me.",
        )
main = parser.add_argument_group('Main options', description="Main options of the program")
main.add_argument('DATE', nargs='*',default=aujourdhui,help="""Theochrone accepts many formats :
                  - Nothing : current day
                  - A complete date with year, month and day of month, for example as following :
                    - DD MM YYYY
                    - DD-MM-YYYY
                    - DD/MM/YYYY
                    - DDMMYYYY
                    - Day in figures, month in letters, year in figures : ex. 30 december 1990 ; 8th july 1990
                    WARNING !!! The order of these elements much depends on your language.
                - You can imply one of these elements, and so works Theochrone :
                    - a figure between 1 and 31 : day of the current month in the current year
                    - a month only (ex : july, sept,...) : the complete month of the current year
                    - the day and the month without year : current year used
                    - a number between 1583 and 4100 : the complete year.
                All of these formats are also accepted by the --from and --to options. (See below)
                    """)
main.add_argument('--from',dest='DEPUIS',nargs='*',default=1,help="""With --to option, --from option can be used to point out the beginning of the period you want to print.
                  Arguments accepted have exactly the same format as DATE (see above).
                  --from may be implied : if --to point out a date later than the current day,
                  --from would automatically considered to be the current day ;
                  else, it would be the first of january of the current year.""" )
main.add_argument('--to',dest='JUSQUE',nargs='*',default=1,help="""With --from option, --to option can be used to point out the end of the period you want to print.
                  Arguments accepted have exactly the same format as DATE (see above).
                  --to may be implied : if --from point out a date prior to the current day,
                  --to would automatically considered to be the current day ;
                  else, it would be the 31st of december of the current year.""")
main.add_argument('-r','--reverse',dest='INVERSE',nargs='*',default=1,help="""Alpha. Does not work properly. Reverse is to be a way to find and print feast by entering their names as arguments, ex : -r Easter, -r 21 Sunday after Pentecosten,... Every other options should be available with this one.""")

affichage = parser.add_argument_group('Print options',description="Convenient options for printing results")
affichage.add_argument('-v','--verbose', help="make theochrone more verbose. Equals to -cdtsLD, and more.",action='store_true')
affichage.add_argument('-c','--color','--colour', dest='couleur', help="print liturgical colour", action='store_true')
affichage.add_argument('-d','--degree', dest='degre', help='print degree of the liturgical feast', action='store_true')
affichage.add_argument('-w','--weekday', dest='jour_semaine',help='print weekday',action='store_true') # not yet available
affichage.add_argument('-t','--transfert', dest='transfert', help='print wether the feast was transfered', action='store_true')
affichage.add_argument('-s','--temporsanct',dest='temporal_ou_sanctoral', help='print whether the feast belongs to the sanctorum or de tempore', action='store_true')
affichage.add_argument('-L','--liturgical-time', dest='temps_liturgique',help='print to which liturgical time the feast belongs to',action='store_true')
affichage.add_argument('-D','--print-date',dest='date_affichee',help='print date',action='store_true')
affichage.add_argument('-l','--language', dest='langue', action='store', help="choose your language /!\ ONLY FRENCH AVAILABLE /!\ ", default = adjutoria.default_language(),choices=['francais','english'])

selection = parser.add_argument_group('Selection options',description="Options to focus researches")
selection.add_argument('-p','--proper','--rite', dest='propre', help='select which proper or rite you want to use',action='store',default='romanus',choices=['romanus','all'])
selection.add_argument('-o','--ordo', dest='ordo', help='select which ordo you want to use', type=int, action='store',default=1962,choices=[1962])
selection.add_argument('-m','--more',dest='plus', help='used with -r/--reverse, print a more complete list of feasts matching with arguments entered', action='store_true')

system = parser.add_argument_group('System options', description="Other options for developers")
system.add_argument('--version', action='version',version='%(prog)s 0.1')
system.add_argument('--test',help='Do not run',action='store_true')
system.add_argument('--poems',help='open O Crux ave Spes Unica', action='store_true')

args = parser.parse_args()

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

mois_seul = False
annee_seule = False
if args.DEPUIS == 1 and args.JUSQUE == 1:
    if isinstance(args.DATE, datetime.date):
        date=args.DATE
    else:
        date, mois_seul, annee_seule = adjutoria.datevalable(args.DATE,args.langue)
else:
    date = 'fromto'
    if args.DEPUIS != 1:
        args.DEPUIS, mois_seul, annee_seule = adjutoria.datevalable(args.DEPUIS,args.langue)
        if args.JUSQUE == 1 and args.DEPUIS <= aujourdhui:
            args.JUSQUE = aujourdhui
        elif args.JUSQUE == 1:
            args.JUSQUE = datetime.date(args.DEPUIS.year,12,31)
            
    if args.JUSQUE != 1 and not isinstance(args.JUSQUE,datetime.date):
        args.JUSQUE, mois_seul, annee_seule = adjutoria.datevalable(args.JUSQUE,args.langue)
        if args.DEPUIS == 1 and args.JUSQUE >= aujourdhui:
            args.DEPUIS = aujourdhui
        elif args.DEPUIS == 1:
            args.DEPUIS = datetime.date(args.JUSQUE.year,1,1)
        
### Définition de quelques variables ###
if date == 'fromto':
    if args.DEPUIS > args.JUSQUE:
        debut = args.JUSQUE
        fin = args.DEPUIS
    else:
        debut = args.DEPUIS
        fin = args.JUSQUE
elif annee_seule:
    debut = date
    fin = datetime.date(date.year,12,31)
elif mois_seul:
    debut = date
    fin = datetime.date(date.year,date.month,calendar.monthrange(date.year,date.month)[1])
else:
    debut = date
    fin = date

if debut.year < 1600:
    adjutoria.erreur(10,args.langue)
elif fin.year > 4100:
    adjutoria.erreur(11,args.langue)
    
Annee = dict()
ordo=args.ordo


### Analyse des fichiers ###
year = debut.year - 1
while True:
    paques = adjutoria.paques(year)
    for fichier in [file for file in adjutoria.fichiers if file.split('_')[1] == str(ordo) and adjutoria.trouve(args.propre,file.split('_')[0])]:
        Annee = adjutoria.ouvreetregarde(fichier,Annee,ordo,args.propre,year,paques)
    if year == fin.year:
        break
    else:
        year += 1

with open('samedi','rb') as file:
    pic=pickle.Unpickler(file)
    samedi=pic.load()
    
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
        if date > fin:
            break
