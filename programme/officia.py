#!/usr/bin/python3
# -*-coding:Utf-8 -*
import adjutoria, datetime

def fabrique_an(debut,fin,ordo=1962,propre='romanus'):
    """Function which creates a liturgical year emulation. It takes four arguments :
    - debut : a datetime.date for the older date ;
    - fin : a datetime.date for the latest date ;
    - ordo : an integer to select which missal will be used ;
    - propre : a string to select the proper.
    It returns a dict, whose keys are datetime.date, and values are lists containing Fete classes. The dict will not contain Saturday feasts of the Virgin, nor feria days."""
    year = debut.year - 1
    Annee = {}
    while True:
        paques = adjutoria.paques(year)
        for fichier in [file for file in adjutoria.fichiers if file.split('_')[1] == str(ordo) and adjutoria.trouve(propre,file.split('_')[0])]:
            Annee = adjutoria.ouvreetregarde('./data/' + fichier,Annee,ordo,propre,year,paques)
        if year == fin.year:
            break
        else:
            year += 1
            
    return Annee

def inversons(mots_bruts,debut,fin,samedi,plus=False,langue='francais',exit=True):
    """Function which returns a list of feasts matching with mots_bruts. It takes seven args:
    - mots_bruts : a string for the research ;
    - debut : a datetime.date for the older date ;
    - fin : a datetime.date for the latest date ;
    - samedi : the Saturday of the Virgin Fete ;
    - plus : a bool to define whether the results will be larger or not ;
    - langue : language used ;
    - exit : a bool to define whether the system have to exit or not in case of error ;
    """
    Annee = fabrique_an(debut,fin)
    if isinstance(mots_bruts,list):
        mots_bruts = [adjutoria.sans_accent(mot) for mot in mots_bruts]
    else:
        mots_bruts = adjutoria.sans_accent(mots_bruts).split()
    mots = []
    for mot in mots_bruts:
        if ' ' in mot:
            mots = mots + mot.split()
        else:
            mots = mots + [mot]
    mots = adjutoria.modification(mots,langue)
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
            Annee[date] = adjutoria.selection(Annee[date],date,Annee,samedi)
            for fete in Annee[date]:
                fete.valeur = fete.Correspondance(mots_str,mots)
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
        liste = [adjutoria.erreur(20,langue,exit=exit)]
    
    return liste
