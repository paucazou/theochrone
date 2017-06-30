#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import enc
import os
import sys

os.chdir("Dossier d'objets")
file_name = 'romanus_1962_dimanches.xml'
with enc.Preferences(file_name,'r') as file:
    liste = file.prefs

for i, elt in enumerate(liste):
    print(i,elt,getattr(elt,'station',False))

choice =int( input('Choisissez où commencer') )

n=choice
for elt in liste[choice:]:
    print(elt)
    answer = input("Voulez-vous quitter(1), ajouter (2),passer (autre réponse)")
    if answer == '2':
        fr_name = input("Rentrez le nom de la station")
        elt.station = {'latina':'','english':'','francais':fr_name}
    elif answer == '1':
        anwer = input("Voulez-vous enregistrer: Y/n")
        if answer != "n":
            with enc.Preferences(file_name,'w') as file:
                file.prefs = liste
        sys.exit()
    n+=1
