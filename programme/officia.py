#!/usr/bin/python3
# -*-coding:Utf-8 -*
import adjutoria

def fabrique_an(debut,fin,ordo=1962,propre='romanus'):
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
