#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
# Deus, in adjutorium meum intende.
import copy
import calendar
import datetime
import json
import messages
import officia
import os
import re
import sys

msg = messages.translated_messages('adjutoria')
liturgiccal = calendar.Calendar(firstweekday=6)
file_folder = os.path.dirname(os.path.abspath(__file__))
if messages.args.gui or not 'theochrone' in sys.argv[0]:
    import pickle
    with open(file_folder+'/data/images.pic','rb') as file:
        images = pickle.Unpickler(file).load() # Un dictionnaire, prenant pour clef Fete._images et pour valeur une liste d'objets imagines.Images

#import pdb ; pdb.set_trace()


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
        self._couleur='blanc' # vert par défaut 
        self.date_='' # un élément qui permet de calculer la date

        self.personne='deuxieme' # indique quel saint ou personne divine est célébrée. Très important pour le classement.
        self.fete_du_Seigneur=False
        
        self.occurrence_perpetuelle=False # Pour toutes les fêtes souffrant d'une occurrence perpetuelle avec une autre fête.
        self.dimanche=False # Pour les dimanches
        self.repris_en_ferie=False # Pour les jours qui sont repris en férie
        
        self.temporal=False
        self.sanctoral=False
        #self.station = {'francais':'','latina':'','english':''} # Station name, for temporal only
        self._temps_liturgique = 'variable' # un élément qui permet de connaître le temps liturgique
        
        self.link=str() # un lien vers Introibo, en attendant une classe spéciale textes.
        self.textes='' # Textes de la messe et des Vêpres, pour plus tard
        self._images='' # La clef qui doit être utilisée pour retrouver les images
        self.addendum={'francais':'',
                       'english':'',
                       'latina':'',
                       } # à ajouter à l'affichage. Par exemple, fête de la dédicace : priorité uniquement pour l'église en question.

        self.pal=False # pal=Pro aliquibus locis
        self.votive=False # Si la messe est votive
        self.peut_etre_votive=False # Si la messe peut être reprise comme votive
        
        #Éléments variables selon l'année
        self.peut_etre_celebree=False
        self._transferee=False
        self.date=None # la date effective
        self.date_originelle=None # en cas de transfert
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
        self.valeur=int() # the value returned by Correspondance
        # parent
        self.parent = None

    # Définitions de certaines méthodes spéciales
    def __str__(self):
        """Méthode affichant des informations sur l'objet grâce à print"""
        return """{}, fête de {} classe selon le missel de {}.""".format(self.nom['latina'],self.degre,self.ordo)
    def __repr__(self):
        """Méthode affichant le nom de l'objet"""
        return self.nom['latina']
    def __lt__(self,autrefete): # TEST
        """Méthode pour comparer les objets ensemble, et surtout pour les trier dans la liste (via un list.sort().)""" # Je crains que cette fonction ne serve à rien.
        if self.degre == autrefete.degre:
            return self.priorite > autrefete.priorite
        else:
            return self.degre < autrefete.degre
        
    def __eq__(self,autrefete): # TEST
        """Méthode pour comparer deux objets type Fete"""
        if isinstance(autrefete,Fete):
            return self.__dict__ == autrefete.__dict__
        else:
            raise TypeError("""{} is not a 'Fete' class, or any of her subclasses.""".format(autrefete))
        
    def __hash__web(self): # méthode très mauvaise, mais seule utilisable actuellement pour le web
        """Méthode appellée par la fonction hash()"""
        hash_list = []
        for item in self.__dict__.values():
            if isinstance(item,dict):
                hash_list += [ str(itemtwo) for itemtwo in item.values() ]
            else:
                hash_list.append(item)
        return hash(str(hash_list))
    
    def __hash__(self): # TEST pose problème pour les datetime
        """Method called by hash() function"""
        print(self)
        parent = self.parent
        del(self.parent)
        hache = hash(json.dumps(self.__dict__,sort_keys=True))
        self.parent = parent
        return hache
        
    # Définitions de méthodes   
    def Votive(self):
        """Une fonction calculant quels jours on peut célébrer la messe votive. Que renvoie-t-elle ?"""
        pass
    
    def DateCivile_(self,paques,annee):
        pass
    
    def copy(self): # TEST
        """Une fonction qui renvoie un autre objet"""
        renvoye = self.__class__()
        renvoye.__dict__ = self.__dict__.copy()
        return renvoye
    
    def DateCivile(self,paques,annee): # TEST
        """Une fonction qui va tester si la date est déjà déterminée,
        sinon il va la demander à la fonction DateCivile_()"""
        if not isinstance(self.date,datetime.date):
            self.date = self.DateCivile_(paques,annee)
        return self.date
    
    def weeknumber(self,month=True,year=False): # TEST
        """Calcule à quelle semaine appartient la fête.
        Si month == True, renvoie la semaine dans le mois.
        Si year == True, renvoie la semaine dans l'année.
        Si tous les deux sont True or False,
        renvoie une tuple avec le mois puis l'année."""
        wn = lambda x : [i + 1 for i, week in enumerate(liturgiccal.monthdayscalendar(x.year,x.month)) if x.day in week][0]
        wn = wn(self.date)        
        firstday = datetime.date(self.date.year, 1, 1)
        if firstday.weekday() > 3:
            firstday = firstday + datetime.timedelta(7 - firstday.isoweekday())
        else:
            firstday = firstday - datetime.timedelta(firstday.isoweekday())
        wy = int(((self.date - firstday).days / 7) + 1) # TODO à vérifier
        if month and year or not month and not year:
            return wn, wy
        elif month:
            return wn
        else:
            return wy
    
    def DatePaques(self,paques,annee): # TEST
        """Une fonction qui calcule le nombre de jours par rapport à Pâques"""
        return paques - self.date
    
    def Correspondance(self,mots,mots_separes,plus):
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
            elif index == 'refus_faible' and not plus:
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
                    elif index == 'refus_fort' and not plus:
                        niveau -= 15 # 15 normalement
                    elif index == 'annexes':
                        niveau + 20
                
                for mot in mots_separes: # cela pose problème pour certaines regex, qui sont composées de deux mots. (in albis par exemple)
                    if a.fullmatch(mot):
                        if 'refus' in index:
                            if not plus:
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
    
    def temps_liturgique(self): # TEST
        """Une fonction qui renvoie le temps liturgique"""
        if self._temps_liturgique == 'variable':
            date = self.date
            while True:
                try:
                    for a in self.parent[date]:
                        if a.temporal:
                            return a._temps_liturgique
                    date = date - datetime.timedelta(1)
                except KeyError:
                    date = date - datetime.timedelta(1)
                    continue
        else:
            return self._temps_liturgique
    
    # Définitions de propriétés
    def _get_priorite(self):
        """Une fonction pour renvoyer self._priorite."""
        return self._priorite
    
    priorite = property(_get_priorite)

    def _get_couleur(self):
        """Une fonction qui calcule la couleur des ornements"""
        return self._couleur
    
    couleur = property(_get_couleur)
    
    def _set_transferee(self,value): # TEST
        """Une méthode qui modifie la valeur de self.transferee
        et fait les modifications nécessaires."""
        self._transferee = value
        if value and not self.date_originelle:
            self.date_originelle = self.date
        self.date = self.date + datetime.timedelta(1)
        
    def _get_transferee(self):
        """Renvoie la valeur de self._transferee"""
        return self._transferee
    
    transferee = property(_get_transferee,_set_transferee)
    
    def _get_images(self): # TEST
        """Renvoie une liste d'images en recherchant dans le dossier images
        tout ce qui correspond à la liste contenue dans self._images.
        Si la liste est vide, renvoie None"""
        if not self._images or not images.get(self._images):
            return None
        else:
            return images[self._images]
        
    images = property(_get_images)
    
    hache = property(__hash__web)
    
class FeteFixe(Fete):
    """Une classe définissant une fête fixe, c'est-à-dire dont la date ne change pas dans l'année."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_={
            'mois':int(),
            'jour':int(),
            }           
    
    def DateCivile_(self,paques,annee): # TEST
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
            
    def DateCivile_(self,paques,annee): # TEST
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
    
    def DateCivile_(self,paques,annee): # TEST
        """Calcule la date civile d'une fête mobile."""
        return paques + datetime.timedelta(self.date_)
    
class FeteMobileDerniersDimanchesPentecote(Fete):
    """Une classe définissant les derniers dimanches après la Pentecôte, à partir du 23 ème."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_={} # un dictionnaire prenant pour clef le nombre de jours entre Pâques et le quatrième dimanche de l'Avent, et en valeur le nombre de jours entre Pâques et le jour de la fête.
    
    def DateCivile_(self,paques,annee):  # TEST
        """Calcule la date par rapport à Pâques et Noël."""
        ecart = officia.dimancheavant(datetime.date(annee,12,25)) - paques
        try:
            return paques + datetime.timedelta(self.date_[ecart.days])
        except KeyError:
            self._priorite = 0
            return paques + ecart - datetime.timedelta(28) # renvoie au dernier dimanche après la Pentecôte.
    
class FeteMobileAvent(Fete):
    """Une classe définissant les fêtes de l'Avent. On pourrait les faire basculer dans les derniers dimanches après la Pentecôte."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_=int() # Un entier correspondant au nombre de jours par rapport au quatrième dimanche de l'Avent. + = avant, - = après # Incohérent
        
    def DateCivile_(self,paques,annee): # TEST
        """Calcule la date civile en fonction du nombre de jours d'écart avec le quatrième dimanche de l'Avent."""
        retour= officia.dimancheavant(datetime.date(annee,12,25)) - datetime.timedelta(self.date_)
        self.nom_passager = {}
        for langue in self.nom:
            self.nom_passager[langue] = officia.nom_jour(retour,langue)
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
    
    def DateCivile_(self,paques,annee): # TEST
        """Calcule la date par rapport à Pâques et au premier dimanche après l'Epiphanie."""
        septuagesime = paques - datetime.timedelta(63)
        retour= officia.dimancheapres(datetime.date(annee,1,6)) + datetime.timedelta(self.date_)
        if retour > septuagesime:
            retour = septuagesime
            self._priorite = 0
            self.commemoraison_privilegiee = -1
        return retour
    
    def _get_couleur(self): # TEST
        if self.date >= datetime.date(self.date.year,1,14):
            return 'vert'
        else:
            return self._couleur
        
    couleur = property(_get_couleur)

class FeteMobileMois(Fete):
    """Une classe définissant une fête qui se calcule en fonction de sa place dans un mois particulier.
    self.date contient un dictionnaire à trois entrées : le numéro de mois, le jour de la semaine(0=lundi), et un chiffre représentant son ordre d'apparition dans le mois (0 représente la première semaine, -1 représente la dernière)
    Exemple: { 'mois' : 10, 'jour': 6, 'ordre': 0} = premier dimanche du mois d'octobre."""
    
    def __init__(self):
        Fete.__init__(self)
        self.date_={
            'mois' : 1,
            'jour' : 0,
            'ordre' : -1,
            }
        
    def DateCivile_(self,paques,annee): # TEST
        """Calcule la date civile."""
        jouran = calendar.monthcalendar(annee,self.date_['mois'])[self.date_['ordre']][self.date_['jour']]
        
        if jouran == 0 and self.date_['ordre'] > -1:
            jouran = calendar.monthcalendar(annee,self.date_['mois'])[self.date_['ordre'] + 1][self.date_['jour']]
        elif jouran == 0 and self.date_['ordre'] < 0:
            jouran = calendar.monthcalendar(annee,self.date_['mois'])[self.date_['ordre'] - 1][self.date_['jour']]
            
        return datetime.date(annee,self.date_['mois'],jouran)
    
class FeteFixeTransferablePaques(FeteFixe): # DEPRECATED
    """Une classe pour toutes les fêtes fixes qui peuvent être transférées et dont la date se calculera par rapport à Pâques.""" #Pour l'Annonciation et les litanies majeures ; sans doute inutile : le système de base devrait suffire, puisque les fêtes sont de première classe
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.borne_debut=int()
        self.borne_fin=int()
        self.transfert=int()
    
    def DateCivile_(self,paques,annee):
        """Une fonction calculant la date civile."""
        datedebase=datetime.date(annee,self.date_['mois'],self.date_['jour'])
        if datedebase < paques + datetime.timedelta(self.borne_debut) or datedebase > paques + datetime.timedelta(self.borne_fin):
            return datedebase
        else:
            return paques + datetime.timedelta(self.transfert)
        
class FeteFixeTransferableDimanche(FeteFixe):
    """Une classe pour toutes les fêtes fixes qui peuvent être transférées et dont la date sera un dimanche."""
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.ecart_dimanche=int() # combien de dimanches d'écart ; 0 : le dimanche se trouve dans la même semaine
        self.apres=True # indique s'il faut voir le dimanche d'avant ou d'après
        
    def DateCivile_(self,paques,annee): # TEST
        """Une fonction calculant la date civile."""
        date_fixe = datetime.date(annee,self.date_['mois'],self.date_['jour'])
        if self.apres:
            return officia.dimancheapres(date_fixe) + datetime.timedelta(self.ecart_dimanche*7)
        else:
            return officia.dimancheavant(date_fixe) - datetime.timedelta(self.ecart_dimanche*7)
        
class FeteMobileCivile(FeteFixe):
    """Une classe pour toutes les fêtes qui dépendent d'un jour de l'année précis, mais mobiles dans la semaine"""
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.semaine = int() # un numéro correspondant au nombre de semaines d'écart # TODO useless ?
        self.jour_de_semaine=int() # un numéro correspondant au jour (0=dimanche)
        
    def DateCivile_(self,paques,annee): # TEST
        """Une fonction calculant la date civile"""
        calendrier = calendar.Calendar(firstweekday=6)
        mois = calendrier.monthdatescalendar(annee,self.date_['mois'])
        for i,semaine in enumerate(mois):
            for jour in semaine:
                if jour == datetime.date(annee,self.date_['mois'],self.date_['jour']):
                    return mois[i][self.jour_de_semaine]     
        
class FeteFerie(Fete):
    """Une classe définissant des jours de férie, comprenant une liste de dates en dehors des fêtes fixes."""
    
    def __init__(self):
        Fete.__init__(self)
        self.degre=4
        self._priorite=200
        self.commemoraison_privilegiee=-1
        self.temporal = True
    
    def QuelNom(self,jour): # TEST
        """Une fonction qui renvoie le nom qui doit être donné au jour de férie."""
        return {'latina': officia.nom_jour(jour,'latina').capitalize(),
                'francais':officia.nom_jour(jour,'francais').capitalize() + ' de la férie du ' + officia.affiche_temps_liturgique(self,'francais'),
                'english':officia.nom_jour(jour,'english').capitalize()} # Comment dit on jour de férie en anglais ? feria (Saturday ?)
    
    def Dimanche_precedent(self,jour,Annee): # DEPRECATED
        """Une fonction qui renvoie le dimanche précédent, si la férie est attestée, et change son nom, sa classe, priorite, et commemoraison_privilegiee.""" # changer cette aide
        curseur = jour
        boucle = True
        while boucle:
            curseur = curseur - datetime.timedelta(1)
            if curseur.year < jour.year and curseur.year not in Annee:
                liste = Annee.previous_year_data[curseur.year][curseur]
            else:
                liste = Annee[curseur]
            try:
                for office in liste:
                    if office.repris_en_ferie:
                        nouveau = self.__class__()
                        nouveau.date=jour
                        nouveau.propre = office.propre
                        nouveau.link = office.link
                        nouveau.addendum = office.addendum
                        if jour >= datetime.date(jour.year,1,14) and office.temps_liturgique == 'epiphanie':
                            nouveau._temps_liturgique = 'apres_epiphanie'
                            nouveau._couleur = 'vert'
                        else:
                            nouveau._temps_liturgique = office._temps_liturgique
                            nouveau._couleur = office.couleur
                        try:
                            nouveau.nom = nouveau.QuelNom(jour)
                        except IndexError:
                            nouveau.nom = 'dimanche'
                        nouveau.parent = Annee
                        return nouveau
            except KeyError:
                continue
            
    def CreateFeria(self,day,lcalendar): # TEST
        for feast_list in lcalendar.unsafe_iter(stop=day,reverse=True):
            if feast_list:
                for office in feast_list:
                    if office.repris_en_ferie:
                        nouveau = self.__class__()
                        nouveau.date=day
                        nouveau.propre = office.propre
                        nouveau.link = office.link
                        nouveau.addendum = office.addendum
                        if day >= datetime.date(day.year,1,14) and office.temps_liturgique == 'epiphanie':
                            nouveau._temps_liturgique = 'apres_epiphanie'
                            nouveau._couleur = 'vert'
                        else:
                            nouveau._temps_liturgique = office._temps_liturgique
                            nouveau._couleur = office.couleur
                        nouveau.nom = nouveau.QuelNom(day)
                        nouveau.parent = lcalendar
                        return nouveau
            
class Samedi(Fete):
    """Une fête définissant l'office de la sainte Vierge du samedi"""
    
    def Est_ce_samedi(self,jour): # TEST
        """Une fonction qui renvoie un booléen si le jour considéré est un samedi"""
        if datetime.date.isoweekday(jour) == 6:
            self.date = jour
            return True
        else:
            return False
    
#classe de fêtes sui generis
class TSNJ(FeteFixe):
    """Une classe définissant la fête du Très Saint Nom de Jésus, et toutes celles qui lui ressemblent."""
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.limite_basse=2
        self.limite_haute=5 # les limites correspondent à des jours pendant lesquels la fête est susceptible de tomber
        
    def DateCivile_(self,paques,annee): # TEST
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
        
    def _get_priorite(self): # TEST
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
        
    def DateCivile_(self,paques,annee): # TEST
        """Calcule la date civile en fonction du premier dimanche après Noël."""
        if officia.dimancheapres(datetime.date(annee,12,25)) == datetime.date(annee + 1,1,1):
            self._priorite = 0
        return officia.dimancheapres(datetime.date(annee,12,25))
    
# classes de fêtes à plusieurs dates

class JoursOctaveDeNoel(FeteFixe):
    """Une classe pour les jours dans l'Octave de Noël"""
    
    def __init__(self):
        FeteFixe.__init__(self)
        self.nom_={'francais':"jour dans l'Octave de Noël",'latina':'Die infra octavam Nativitatis','english':'day in the Octave of Christmas'} 
        self.complements_nom={'francais':['Deuxième','Troisième','Quatrième','Cinquième','Sixième','Septième'],
                              'latina': ['De Secunda','De Tertia','De Quarta','De Quinta', 'De Sexta','De Sabbato'],
                              'english': ['Secund','Third','Fourth','Fifth','Sixth','Seventh',]
                              }
        self.date_=[26,27,28,29,30,31]
        self.mois_ = 12
        
    def DateCivile(self,paques,annee): # TEST
        """Renvoie une liste de dates"""
        objets = []
        regex = self.regex
        del(self.__dict__['regex'])
        for i,a in enumerate(self.date_):
            retour = FeteFixe()
            retour.__dict__ = copy.deepcopy(self.__dict__)
            retour.regex = officia.renvoie_regex(retour,regex,[i])
            retour.date = datetime.date(annee,self.mois_,self.date_[i])
            for langue in ('francais','latina','english'):
                retour.nom[langue] = self.complements_nom[langue][i] + ' ' + self.nom_[langue]
            yield retour

class JoursAvent(FeteMobileAvent):
    """Une classe pour les jours de férie de l'Avent"""
    pass

    def __init__(self):
        FeteMobileAvent.__init__(self)
        self.date_ = [-1,-2,-3,-4,-5,
                      3,5,6,
                      8,9,10,11,12,13,
                      15,16,17,18,19,20,]
        self.nom_ = {"francais":["de la première semaine de l'Avent","de la deuxième semaine de l'Avent","de la troisième semaine de l'Avent","de la quatrième semaine de l'Avent"],
                        "english": ['of the first week of Advent','of the second week of Advent','of the third week of Advent','of the fourth week of Advent'],
                        "latina": ['infra primam Hebdomadam Adventus', 'infra secondam Hebdomadam Adventus','infra tertiam Hebdomadam Adventus','infra quartam Hebdomadam Adventus'],
                        }
        
    def DateCivile(self,paques,annee): # TEST
        """Renvoie une liste d'objets"""
        objets = []
        regex = self.regex
        del(self.__dict__['regex'])
        for a in self.date_:
            retour = FeteMobileAvent()
            retour.__dict__ = copy.deepcopy(self.__dict__)
            retour.date_ = a
            retour.date = retour.DateCivile(paques,annee)
            for langue in ('latina','english','francais'):
                retour.nom[langue] = retour.nom_passager[langue].capitalize() + ' '
                if a > 14:
                    retour.nom[langue] += self.nom_[langue][0]
                    semaine = 1
                elif a > 6 and a < 15:
                    retour.nom[langue] += self.nom_[langue][1]
                    semaine = 2
                elif a > 0 and a < 7:
                    retour.nom[langue] += self.nom_[langue][2]
                    semaine = 3
                else:
                    retour.nom[langue] += self.nom_[langue][3]
                    semaine = 4
            retour.regex = officia.renvoie_regex(retour,regex,[retour.nom_passager[langue],semaine])
            if retour.date.day > 16:
                retour.degre = 2
                retour._priorite = 1200
            yield retour
    
class SeptEmber(Fete): # WARNING WARNING WARNING
    """A class defined to fix an error. Must be changed asap"""
    
    def __init__(self,weekday=3):
        Fete.__init__(self)
        self.sunday = 3
        self.month = 9
        self.weekday = weekday # firstweekday = sunday = 0
        
    def DateCivile_(self,paques,annee):
        """Method returning date"""
        lcalendar = calendar.Calendar(firstweekday=6)
        i = 0
        for week in lcalendar.monthdayscalendar(annee,self.month):
            if week[0] > 0:
                i+=1
            if i == 3:
                return datetime.date(annee,self.month,week[self.weekday])
        
        


    

