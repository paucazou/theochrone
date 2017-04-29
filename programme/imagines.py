#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

class Images:
    """Classe conteneur des informations sur les images utilisées associées aux fêtes."""
    def __init__(self):
        self.link = '' # adresse relative de l'image. Toutes sont contenues dans le répertoire images/fetes
        self.titre = {'francais':'','english':'','latina':''} # Titre de l'image qui sera affichée
        self.auteur = {'francais':'','english':'','latina':''} # Nom de l'auteur, s'il y a lieu
