#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from sys import argv, exit
import adjutoria
import variables
import enc
import pickle
import readline
import os
import subprocess
import re
import random
import argparse
import copy

parser = argparse.ArgumentParser(
        prog='Caisse',
        formatter_class=argparse.RawTextHelpFormatter,
        description="""A tool to create, modify, delete and save objects as xml or pickle for Theochrone""",
        )

parser.add_argument('-x','--xtopic', help="transform xml files in pickle ones fastly",action='store_true')
parser.add_argument('-i','--indent', help="indent all xml files in Dossier d'objets",action='store_true')
parser.add_argument('-d','--debug', help="debug the script",action='store_true')
args = parser.parse_args()

objets = []
objets_ancien = []
ajout = []
fichier = 'non'
fichier_tmp = '.tmp-'+ str(random.randrange(0,500)) + '-' + str(adjutoria.datetime.date.today()) + '.xml'
MENU = "menu"
COMMAND = "command"
EQUAL = "equal"
ARGS = 'args'

if os.getcwd().split('/')[-1] == 'programme' or os.getcwd().split('/')[-1] == "Dossier d'objets":
    os.chdir('..')
     
def menu(donnee,parent=None,direct_exit=False,renvoi=False):
    exitmenu = False
    while not exitmenu:
        print(donnee['title'],'\n',donnee['subtitle'],'\n')
        for i, elt in enumerate(donnee['options']):
            print("""{}. {}.""".format(i, elt['title']))
        if parent == None:
            print('{}. Quitter'.format(i+1))
        else:
            print('{}. Revenir au menu précédent'.format(i+1))
        reponse = input()
        try:
            reponse = int(reponse)
        except:
            print("""Réponse invalide.""")
            continue
        if reponse > i + 1:
            print("""Réponse invalide.""")
            continue
        elif reponse == i + 1:
            if parent == None:
                depart()
            else:
                exitmenu = True
        elif donnee['options'][reponse]['type'] == MENU:
            if renvoi:
                return menu(donnee['options'][reponse],donnee,renvoi=True)
            else:
                menu(donnee['options'][reponse],donnee)
        elif donnee['options'][reponse]['type'] == COMMAND:
            if 'arg2' in donnee['options'][reponse]:
                donnee['options'][reponse]['command'](donnee['options'][reponse][ARGS],donnee['options'][reponse]['arg2'])
            elif ARGS in donnee['options'][reponse]:
                donnee['options'][reponse]['command'](donnee['options'][reponse][ARGS])
            else:
                donnee['options'][reponse]['command']()
        elif donnee['options'][reponse]['type'] == EQUAL:
            if 'args2' in donnee['options'][reponse]:
                return donnee['options'][reponse][ARGS], donnee['options'][reponse]['args2']
            elif ARGS in donnee['options'][reponse]:
                return (donnee['options'][reponse][ARGS])
        if direct_exit:
            exitmenu = True
    
    
def depart():
    correspondance = True
    if fichier != 'non':
        if objets_ancien != objets:
            correspondance = False
    if ajout == [] and correspondance:
        print("""Au revoir""")
        exit()
    if ajout != []:
        print('Vous avez créé des objets : ')
        for a in ajout:
            print(a.nom['latina'])
    if not correspondance:
        print('Vous avez modifié des objets : ')
        for a in objets:
            if a not in objets_ancien:
                print(a.nom['latina'])
    reponse = input("""Voulez-vous :
        - QUITTER sans enregistrer ?
        - ENREGISTRER puis quitter ?
        - Revenir au menu principal [par défaut] ?\n""")
    if reponse == 'QUITTER':
        print('Modifications abandonnées. \nAu revoir')
        exit()
    elif reponse == 'ENREGISTRER':
        sauvegarde()
        print('Modifications enregistrées. \nAu revoir')
        exit()
    else:
        pass  
    
def finput(prompt='>>> ', text=''):
    text = str(text)
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt + '\n')
    readline.set_pre_input_hook()
    return result

def CompileRegex(objet):
    """Fonction de compilation des regex""" # énormément d'erreurs dans cette fonction = certaines regex font n'importe quoi, et certains titres ne sont pas supprimés.
    
    vaisseau = copy.deepcopy(objet.regex_)
    titres = ['saint([^e]|$|\.|\?)', 'sainte', 'saints','saintes','bienheureux', 'bienheureuse([^s]|$|\.|\?)','bienheureuses.',
              'lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche','janvier','février','mars','avril','mai$', 'juin','juillet','août','septembre','octobre','novembre','décembre',]
    syntaxiques=['de','à','l','le','d','des','du'] #ne pas mettre des mots qui pourraient se trouver dans les annexes : du, après, à,l'
    chiffres = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',]

    annexes = [] # Il faudrait quelque chose de ce genre pour les jours de la semaine, et les données modifiables peut-être lancer la recherche directement depuis la fonction de traitement des données : oui, une recherche par caractéristiques ; cela ne fait pas doublet, mais permet de faire des recherches approximatives.
    annexes.append(objet._couleur)
    if objet.degre == 5:
        annexes += ['(mémoire|commémoraison)']
        titres.append('privilégiée')
    else:
        annexes.append(str(objet.degre) +'classe')
    if objet.commemoraison_privilegiee > 0:
        annexes += ['(mémoire|commémoraison).*privilégiée']
    if objet.fete_du_Seigneur:
        annexes += ['fêtes?(du)?.*seigneur']
    if objet.temporal:
        annexes.append('temporal')
    else:
        annexes.append('sanctoral')
    if isinstance(objet._temps_liturgique,str):
        annexes.append("temps.*" + re.sub('_','.*',objet._temps_liturgique))
    else:
        for item in objet._temps_liturgique:
            annexes.append("temps.*" + re.sub('_','.*',item))
    if objet.pal:
        annexes.append('pro.*aliquibus.*locis')
    if objet.votive:
        annexes.append('votives')
        
    vaisseau['annexes'] = annexes
        
    
    for liste in vaisseau.values():
        for value in liste:
            for i,a in enumerate(syntaxiques):
                if value == a:
                    del(syntaxiques[i])
            for i, a in enumerate(chiffres): # normalement, cette partie devrait permettre d'exclure seulement les nombres correspondants : 10 n'exclue pas 1 et 0, mais seulement 10, 1 suivi d'une lettre, et 0 précédé d'une lettre.
                if value == a:
                    del(chiffres[i])
                elif a in value:
                    if a == value[0]:
                        chiffres[i] = a + "($|[^" + value[1] + "])"
                    elif a == value[1]:
                        chiffres[i] = "(^|[^" + value[0] + "])" + a # tester si ces nouvelles fonctionnalités marchent.
            for i,a in enumerate(titres):
                if re.findall(a,value):
                    del(titres[i])
    if 'refus_fort' in vaisseau.keys():
        vaisseau['refus_fort'] += chiffres + titres
    else:
        vaisseau['refus_fort'] = chiffres + titres
    if 'refus_faible' in vaisseau.keys():
        vaisseau['refus_faible'] += syntaxiques
    else:
        vaisseau['refus_faible'] = syntaxiques
    delete = []
    for index,liste in vaisseau.items():
        if liste == []:
            delete.append(index)
            continue
        for i,mot in enumerate(liste):
            if len(mot) > 4:
                #traitement du [in]
                mot = re.sub("([ae]?i|u)(n|m)($|[^mnaeiouy])",r"([ae]?i|u)(n|m)\3",mot)
                #traitement du i
                mot = re.sub("(y|i)","(y|i)",mot)
                #traitement du son [o]
                mot = re.sub("(ô|o($|[^nm])|e?au)",r"(o|e?au)\2",mot)
                #traitement du œ
                mot = re.sub('œ',r"(oe|œ)",mot)
                #traitement de [on]
                mot = re.sub('o(m([^m])|n([^n]))',r"o(m|n)\2\3",mot)
                #traitement de lettres finales ; on peut y échapper en mettant un point derrière, par exemple, ou un tréma pour le e.
                mot = re.sub('(([^e])t|[dse])$',r"\1?",mot)
                #traitement du h
                mot = re.sub("(^|[^cp])h",r"\1h?",mot)
                #traitement du type [en]
                mot = re.sub('(ea?|a)(m|n)($|[^mnaeiouy])',r"(ea?|a)(m|n)\3",mot)
                # traitement du type é
                mot = re.sub('(é|è|ê|&|[ea][iy]|(et|er)$|e([sx]|nn)|ë(.))',r"(e|&|[ea][iy]|(et|er))\3\4",mot)
                #traitement du [k]
                mot = re.sub("(c($|[^heiy])|(qu?|k))",r"(c|qu|k)\2",mot)
                #traitement du [s]
                mot = re.sub('((^|[^s])s($|[^aous])|c([eiy]))',r"\2(s|c)\3\4",mot) # pris en compte devant a : ça ne marche pas, à revoir
                #traitement de [e]
                mot = re.sub("(eu|e($|[^ts])($|[^nn]))",r"(eu|e)\2\3",mot)
                #traitement des consonnes doubles
                for lettre in 'bcdfglmnprstv':
                    mot = re.sub(lettre+lettre,lettre+lettre+'?',mot)
            liste[i]=re.compile(adjutoria.sans_accent(mot))
        vaisseau[index]=tuple(liste)
    for key in delete:
        if vaisseau[key] == []:
            del(vaisseau[key])
    return vaisseau

def choix_fichier():
    global fichier
    global objets_ancien
    os.chdir("./Dossier d'objets")
    subprocess.run(['ls'])
    readline.parse_and_bind("tab: complete")
    fichier=finput("""Entrez le nom du fichier. Si ce fichier n'existe pas, il sera automatiquement créé. """)
    global objets
    try:
        with enc.Preferences(fichier,'r') as file:
            objets = file.prefs
        print("Fichier {} chargé.".format(fichier))
    except: # Il y a un problème avec le Parser
        objets = []
        print("""Un nouveau fichier sera créé lorsque vous procéderez à l'enregistrement.""")
    objets_ancien = objets.copy()
    os.chdir("..")

def basculer():
    if objets != []:
        os.chdir("./programme")
        subprocess.run(['ls'])
        second_file = finput("""Entrez le nom du fichier dans lequel seront enregistrées les données. S'il n'existe pas, il sera automatiquement créé. """,fichier.split('.')[0]+'.pic')
        with open(second_file,'wb') as f:
            pic = pickle.Pickler(f)
            for a in objets:
                if args.debug:
                    print(a)
                a.regex = CompileRegex(a)
                pic.dump(a)
                print("""{} enregistré.""".format(a.nom))
            input("""Enregistrement terminé""")
    else:
        print("""Vous n'avez actuellement aucun objet. Veuillez choisir un fichier à traiter ou enregistrer préalablement des objets avant de faire la bascule.""")
    os.chdir("..")

def modification():
    global objets
    if objets != []:
        menu_modif = {'title': "Modifier des objets", 'type': MENU, 'subtitle': "Choisissez l'objet que vous voulez modifier.",'options':[]}
        for a in objets:
            menu_modif['options'].append({'title': a.nom['latina'], 'type': COMMAND, 'command': ajouter, ARGS: type(a).__name__, 'arg2':a.__dict__})
        menu(menu_modif,menus)
    else:
        print("""Vous n'avez actuellement aucun objet. Veuillez choisir un fichier à traiter ou enregistrer préalablement des objets avant de faire des modifications.""")
        

def supprimer(numero='NON'):
    global objets
    if numero != 'NON':
        print("""Êtes-vous sûr de vouloir supprimer l'objet {} ? \n
              {}""".format(objets[numero].nom['latina'],objets[numero]))
        reponse = input("""oui/[NON]""")
        if reponse == 'oui':
            del(objets[numero])
            print("""Objet supprimé.""")
        else:
            print("""L'objet a été sauvegardé.""")
    elif objets != []:
        menu_suppr = {'title': "Supprimer des objets", 'type': MENU, 'subtitle': "Choisissez l'objet que vous voulez supprimer.",'options':[]}
        i = -1
        for a in objets:
            menu_suppr['options'].append({'title': a.nom['latina'], 'type': COMMAND, 'command': supprimer, ARGS: i+1})
            i+=1
        menu(menu_suppr,menus,True) # attention, le retour à ce menu est trompeur : il n'est pas actualisé après suppression
    else:
        print("""Vous n'avez actuellement aucun objet. Veuillez choisir un fichier à traiter ou enregistrer préalablement des objets avant de vouloir supprimer des objets.""")

def sauvegarde():
    global ajout
    global objets
    global objets_ancien
    global fichier
    if fichier == 'non':
        choix_fichier()
    os.chdir("./Dossier d'objets")
    if ajout != []:
        print("""Voici les objets ajoutés : """)
        for a in ajout:
            print(a.nom)
            for z,b in sorted(a.__dict__.items()):
                print(z,':',b)
    if objets != [] and objets_ancien != objets:
        print("""Voici les objets modifiés : """)
        for a in objets:
            if a not in objets_ancien:
                print(a.nom)
                for z,b in sorted(a.__dict__.items()):
                    print(z,':',b)
    print(objets is objets_ancien)
    reponse = 'peut-être'
    while reponse != 'non':
        reponse = input("""Voulez-vous sauvegarder ? (oui/non)""")
        if reponse == 'oui':
            objets = objets + ajout
            ajout = []
            with enc.Preferences(fichier,'w') as file:
                file.prefs = objets
            os.system('cat ' + fichier + '|xmllint --format - > tMpXmL && cat tMpXmL > ' + fichier + '&& rm tMpXmL')
            reponse = 'non'
            objets_ancien = objets.copy()
    os.chdir("..")
        
        
    
def ajouter(modele,entrees={}):
    global ajout
    global objets
    nouveau = getattr(adjutoria,modele)()
    numero=-1
    if entrees != {}:
        for i, elt in enumerate(objets):
            if entrees == elt.__dict__:
                numero = i
                print('Pris en compte')
        for hideux,a in nouveau.__dict__.items():
            try:
                nouveau.__dict__[hideux] = entrees[hideux]
            except KeyError:
                pass
    
    boucle = True
    erreur = 'Erreur dans les informations rentrées.'
    
    def valider(text='',prerempli='',typ='int'):
        boucle = True
        while boucle:
            prerempli = finput(text,prerempli)
            try:
                if typ == 'int':
                    return int(prerempli)
                elif typ == 'bool':
                    if prerempli == 'True':
                        return True
                    elif prerempli == 'False':
                        return False
                    else:
                        raise ValueError
            except ValueError:
                print(erreur)
            
    while boucle:
        nouveau.nom['latina'] = finput('Rentrez le nom de la fête en latin',nouveau.nom['latina'])
        nouveau.nom['francais'] = finput('Rentrez le nom de la fête en français',nouveau.nom['francais'])
        nouveau.nom['english'] = finput('Rentrez le nom de la fête en anglais',nouveau.nom['english'])
        nouveau.ordo=valider('Rentrez l\'année de l\'ordo de référence.',nouveau.ordo)
        nouveau.propre = finput('Rentrez le propre de cette fête.',nouveau.propre)
        
        nouveau.degre = valider('Rentrez le degré de la fête (1 à 5)',nouveau.degre)
        print("""Voici les différents degrés de préséance :""")
        for i,a in sorted(variables.priorites.items()):
            print(i,':',a)
        nouveau._priorite = valider('Rentrez le degré de préséance de la fête',nouveau._priorite)
        print("""Voici les différents degrés de commémoraison : """)
        for i,a in sorted(variables.priorites_de_commemoraison.items()):
            print(i,':',a)
        nouveau.commemoraison_privilegiee = valider('Rentrez le degré de commémoraison.',nouveau.commemoraison_privilegiee)
        
        nouveau.pal = valider('La messe peut-elle être Pro aliquibus locis ?',nouveau.pal,'bool')
        nouveau.votive = valider('La messe est-elle votive, ou peut-elle être reprise comme votive ?',nouveau.votive,'bool')
        nouveau.occurrence_perpetuelle = valider('La fête souffre-t-elle d\'une occurrence perpétuelle avec une autre fête ?',nouveau.occurrence_perpetuelle,'bool')
        nouveau.dimanche = valider('La fête tombe-t-elle un dimanche ?',nouveau.dimanche,'bool')
        nouveau.repris_en_ferie = valider('La fête est-elle reprise en férie ?',nouveau.repris_en_ferie,'bool')
        nouveau.fete_du_Seigneur = valider('La fête est-elle une fête du Seigneur ?',nouveau.fete_du_Seigneur,'bool')
        nouveau.temporal = valider('La fête fait-elle partie du Temporal ?', nouveau.temporal,'bool')
        if not nouveau.temporal:
            nouveau.sanctoral = True
        else:
            reponse = finput('Cette fête appartient-elle à un temps liturgique variable ?',nouveau._temps_liturgique)
            if reponse == 'variable':
                nouveau._temps_liturgique = 'variable'
            elif reponse == str(nouveau._temps_liturgique):
                pass
            else:
                menu_temps = {'title': "Temps liturgique", 'type': MENU, 'subtitle': "Choississez le temps liturgique",'options':[]}
                i = 0
                for key, value in variables.temps_liturgiques.items():
                    menu_temps['options'].append({'title': "Temps liturgique : {}".format(value), 'type': EQUAL, ARGS: key})
                    i+=1
                nouveau._temps_liturgique = menu(menu_temps, direct_exit = True,renvoi = True)
                
        nouveau._couleur = finput('Rentrez la couleur de la fête.',nouveau._couleur)
        nouveau.link = finput('Merci de rentrer le lien vers les textes sur le site Introibo.fr',nouveau.link)
        nouveau.personne = finput("""Quelle personne est célébrée dans cette fête ?
            Règles :
            1 - Pour les personnes divines :
                Père = premiere
                Fils = deuxieme
                Saint-Esprit = troisieme
            2 - Pour les saints :
                Sainte Vierge = marie
                Saints anciens = prénom exclusivement, en minuscules, sans le titre.
                    Ex : pierre, paul
                Homonymes : toujours le prénom d'abord ; on ne note ni les prépositions (de,à, au...) ni les articles (le, la...)
                    Ex : jean_baptiste, jean_apotre, jean_croix, jean_chrysostome, jean_aumonier, jean_avila...
                Prénoms composés :
                    Ex : jean-marie, jean-pierre.""",nouveau.personne)
        
        for key, value in nouveau.regex_.items():
            prerempli = ''
            for a in value:
                prerempli += a +' '
            nouveau.regex_[key] = finput("Rentrez les mots-clefs de la partie '{}'. N'oubliez pas de les séparer par des blancs.".format(key),prerempli).lower().split()
        
        if modele == 'FeteFixe' or modele == 'FeteMobileCivile':
            nouveau.date_['mois'] = valider('Rentrez le numéro du mois',nouveau.date_['mois'])
            nouveau.date_['jour'] = valider('Rentrez le jour du mois',nouveau.date_['jour'])
            if modele == 'FeteMobileCivile':
                nouveau.semaine = valider('Rentrez le nombre de semaines d\'écart',nouveau.semaine)
                nouveau.jour_de_semaine = valider("Rentrez le jour de la semaine (dimanche = 0)",nouveau.jour_de_semaine)
        elif modele == 'FeteMobilePaques':
            nouveau.date_ = valider('Rentrez le nombre de jour par rapport à Pâques. Avant Pâques = négatif.',nouveau.date_)
        elif modele == 'FeteFixeBissextile':
            nouveau.date_['bissextile']['mois'] = valider('Rentrez le numéro du mois dans le cas d\'une année bissextile.',nouveau.date_['bissextile']['mois'])
            nouveau.date_['bissextile']['jour'] = valider("Rentrez le numéro du jour du mois dans le cas d'une année bissextile.",nouveau.date_['bissextile']['jour'])
            nouveau.date_['ordinaire']['mois'] = valider("Rentrez le numéro du mois dans le cas d'une année ordinaire.",nouveau.date_['ordinaire']['mois'])
            nouveau.date_['ordinaire']['jour'] = valider("Rentrez le numéro du jour du mois dans le cas d'une année ordinaire.",nouveau.date_['ordinaire']['jour'])        
        elif modele == 'FeteMobileDerniersDimanchesPentecote':
            print("""Choisissez quel dimanche vous voulez créer.""")
            for i,a in enumerate(variables.derniers_dimanches_apres_pentecote[0][1:]):
                i +=1
                print("""{}. {}.""".format(i,a))
            boucle_trois = True
            while boucle_trois:
                reponse_trois = valider()
                if reponse_trois <= i and reponse_trois > 0:
                    boucle_trois = False
                    for a in variables.derniers_dimanches_apres_pentecote[1:]:
                        if a[reponse_trois] != 0:
                            nouveau.date_[a[0]] = a[reponse_trois]
                else:
                    print('Choix invalide')
                    
        elif modele == 'FeteMobileAvent':
            nouveau.date_ = valider('Rentrez le nombre de jour par rapport au quatrième dimanche de l\'Avent. Le chiffre doit être positif.',nouveau.date_)
        elif modele == 'FeteMobileNoel':
            nouveau.date_ = valider('Rentrez le nombre de jour par rapport au premier dimanche après Noël. Avant ce dimanche = négatif.',nouveau.date_)
        elif modele == 'FeteMobileEpiphanie':
            nouveau.date_ = valider('Rentrez le nombre de jour par rapport au premier dimanche après l\'Épiphanie. Avant ce dimanche = négatif.',nouveau.date_)
        elif modele == 'FeteMobileMois':
            nouveau.date_['mois'] = valider('Rentrez le numéro du mois',nouveau.date_['mois'])
            nouveau.date_['jour'] = valider('Rentrez le numéro du jour de la semaine (lundi = 0)',nouveau.date_['jour'])
            nouveau.date_['ordre'] = valider("Rentrez le rang du jour par rapport au mois. 0 = premier, -1 = dernier.",nouveau.date_['ordre'])
        elif modele == 'FeteFixeTransferablePaques':
            print("""Informations concernant la date de base :""")
            nouveau.date_['mois'] = valider('Rentrez le numéro du mois',nouveau.date_['mois'])
            nouveau.date_['jour'] = valider('Rentrez le jour du mois',nouveau.date_['jour'])
            print("""Informations concernant le transfert de la fête :\n
                Rentrez les bornes de début et de fin par rapport à Pâques de la période pendant laquelle la fête ne pourra pas être célébrée (chiffre négatif si avant Pâques, positif après).""")
            nouveau.borne_debut = valider('Borne de début',nouveau.borne_debut)
            nouveau.borne_fin = valider('Borne de fin',nouveau.borne_fin)
            nouveau.transfert = valider("Rentrez le nombre de jours après Pâques qui doivent être comptés pour le transfert de la fête.",nouveau.transfert)
        elif modele == 'FeteFixeTransferableDimanche':
            print("""Informations concernant la date de base :""")
            nouveau.date_['mois'] = valider('Rentrez le numéro du mois',nouveau.date_['mois'])
            nouveau.date_['jour'] = valider('Rentrez le jour du mois',nouveau.date_['jour'])
            print("""Informations concernant le transfert de la fête :""")
            nouveau.ecart_dimanche = valider("Combien de dimanches d'écart doit-il y avoir ? (0 pour le dimanche suivant la fête, cas le plus fréquent)",nouveau.ecart_dimanche)
            nouveau.apres = valider("La fête transférée se fête-t-elle le dimanche suivant ? (cas le plus fréquent)",nouveau.apres,'bool')
        elif modele == 'FeteFerie': # rien de particulier à rentrer
            pass
        elif modele == 'Samedi': # rien de particulier à rentrer
            pass
        elif modele == 'TSNJ': # rien de particulier à rentrer
            pass
        elif modele == 'Defunts': # rien de particulier à rentrer
            pass
        
        nouveau.addendum['francais'] = finput('Avez-vous des choses à ajouter ? (Laissez vide sinon)',nouveau.addendum['francais'])
        print("""Notre objet {} est construit. Voici ses caractéristiques :""".format(type(nouveau)))
        for a,b in sorted(nouveau.__dict__.items()):
            print(a,':',b)
        print("""Voulez-vous le (V)alider, le (M)odifier ou (A)nnuler ?""". format(type(nouveau),nouveau.__dict__))
        reponse = 'nothing'
        boucle_deux = True
        while boucle_deux:
            reponse=input()
            if reponse == '':
                continue
            elif reponse[0].lower() == 'v':
                with enc.Preferences(fichier_tmp,'w') as tmp:
                    tmp.prefs = ajout + [nouveau]
                os.system('cat ' + fichier_tmp + '|xmllint --format - > tMpXmL && cat tMpXmL > ' + fichier_tmp + '&& rm tMpXmL')
                if numero == -1:
                    ajout.append(nouveau)
                    print("""Objet ajouté.""")
                else:
                    objets[numero]=nouveau
                    print("""Objet modifié.""")
                boucle = False
                boucle_deux = False
            elif reponse[0].lower() == 'm':
                boucle = True
                boucle_deux = False
            elif reponse[0].lower() == 'a':
                print("""Abandon.""")
                boucle = False
                boucle_deux = False


menus = {
  'title': "Menu principal", 'type': MENU, 'subtitle': "Merci de choisir une option",
  'options':[
    { 'title': "Choisir le fichier à traiter", 'type': COMMAND, 'command': choix_fichier },
    { 'title': "Ajouter des éléments", 'type': MENU, 'subtitle' : "Choisissez l'élément à ajouter",
     'options' : [
         {'title': 'Fête fixe', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteFixe'},
         {'title': 'Fête mobile', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteMobilePaques'},
         {'title': 'Fête fixe d\'une année bissextile', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteFixeBissextile'},
         {'title': 'Derniers dimanches après la Pentecôte', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteMobileDerniersDimanchesPentecote'},
         {'title': 'Fêtes de l\'Avent', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteMobileAvent'},
         {'title': 'Fêtes par rapport à Noël', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteMobileNoel'},
         {'title': 'Fêtes par rapport à l\'Epiphanie', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteMobileEpiphanie'},
         {'title': 'Fête en fonction du mois', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteMobileMois'},
         {'title': 'Fête fixe transférable par rapport à Pâques', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteFixeTransferablePaques'},
         {'title': 'Fête fixe transférable un dimanche', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteFixeTransferableDimanche'},
         {'title': 'Férie ordinaire', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteFerie'},
         {'title': 'Office de la Vierge le samedi', 'type': COMMAND, 'command': ajouter, ARGS: 'Samedi'},
         {'title': 'Très Saint Nom de Jésus', 'type': COMMAND, 'command': ajouter, ARGS: 'TSNJ'},
         {'title': 'Défunts', 'type': COMMAND, 'command': ajouter, ARGS: 'Defunts'},
         {'title': 'Jours dans l\'Octave de Noël', 'type': COMMAND, 'command': ajouter, ARGS: 'JoursOctaveDeNoel'},
         {'title': 'Jours de l\'Avent', 'type': COMMAND, 'command': ajouter, ARGS: 'JoursAvent'},
         {'title': 'Fête un jour de semaine par rapport à une date civile', 'type': COMMAND, 'command': ajouter, ARGS: 'FeteMobileCivile'}
         ]
     },
    { 'title': "Modifier des éléments", 'type': COMMAND, 'command': modification },
    { 'title': "Supprimer des éléments", 'type': COMMAND, 'command': supprimer },
    { 'title': "Enregistrer", 'type': COMMAND, 'command': sauvegarde },
    { 'title': "Faire la bascule", 'type': COMMAND, 'command': basculer },
    ]
    }
     
def dossier_d_objets():
    """Une fonction qui charge le contenu des fichiers xml de Dossier d'objets"""
    os.chdir("./Dossier d'objets")
    liste = subprocess.run(['ls'],stdout=subprocess.PIPE)
    liste = liste.stdout.decode().split('\n')
    fichiers = {}
    for file in liste:
        if file.split('.')[-1] != 'xml':
            continue
        try:
            with enc.Preferences(file,'r') as f:
                fichiers[file] = f.prefs
        except:
            exit("L'un des fichiers ne semble pas avoir le bon format, ou bien est corrompu : {}".format(file))
    os.chdir('..')
    return fichiers
    
if args.xtopic:
    fichiers = dossier_d_objets()
    os.chdir("./programme")
    for fichier,obj in fichiers.items():
        with open(fichier.split('.')[0]+'.pic','wb') as f:
            pic = pickle.Pickler(f)
            for a in obj:
                a.regex = CompileRegex(a)
                pic.dump(a)
elif args.indent:
    fichiers = dossier_d_objets()
    for fichier in fichiers:
        os.system('cat ' + fichier + '|xmllint --format - > tMpXmL && cat tMpXmL > ' + fichier + '&& rm tMpXmL')
else:
    menu(menus)





