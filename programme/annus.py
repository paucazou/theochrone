#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import calendar
import datetime
import os
import pickle

chemin = os.path.dirname(os.path.abspath(__file__))

fichiers=(
    'romanus_1962_dimanches.pic',
    'romanus_1962_fetesduseigneur.pic',
    'romanus_1962_cycledenoel.pic',
    'romanus_1962_cycledepaques.pic',
    'romanus_1962_premiertrimestre_sanctoral.pic',
    'romanus_1962_deuxiemetrimestre_sanctoral.pic',
    #'romanus_1962_troisiemetrimestre_sanctoral.pic',
    #'romanus_1962_quatriemetrimestre_sanctoral.pic',
    #'gallicanus_1962_dimanches.pic',
    )

latinus={
    'romanus':{
        'gallicanus':{
            'lugdunensis':{},
            'parisianus':{},
            },
        'italianus':{},
        'testis':{}, # a test proper, only used with the --test arg.
        },
        'dominicanus':{},
        'cartusiensis': {},
        'visigothica':{},
        'ambrosianus':{},
        'cisterciensis':{},
        'bracarenses':{},
        } # contains the pyramid of the propers ; used in the 'remonte' and 'trouve' functions 
        
liturgiccal=calendar.Calendar(firstweekday=6)

class LiturgicalYear():
    """This class is a collection which contains the whole
    liturgical years requested during the time of the program.""" # créer une fonction getitemlight (return false si request non valide, ou erreur)
    instances = []
    
    def __init__(self, proper='romanus',ordo=1962):
        """Init of the instance"""
        self.raw_data = self.load_raw_data(proper,ordo) # tuple which contains the data extracted from files
        self.year_names = [] # an ordered list of the year currently saved in the instance
        self.year_data = {} # a dict which contains the liturgical years themselves.
        
        self.previous_year_names = []
        self.previous_year_data = {}
        self.next_year_names = []
        self.next_year_data = {}
        
        self.ordo = ordo
        self.proper = proper
        
        LiturgicalYear.instances.append(self)
        
    def load_raw_data(self,proper,ordo):
        """Method used only when creating the instance.
        It loads raw data following the 'proper' and the 'ordo' requested.
        Returns a tuple whith the whole data"""
        tmp = list()
        for fichier in [file for file in fichiers if file.split('_')[1] == str(ordo) and self.trouve(proper,file.split('_')[0])]:
            with open(chemin + '/data/' + fichier, 'rb') as file:
                pic=pickle.Unpickler(file)
                while True:
                    try:
                        tmp.append(pic.load())
                    except EOFError:
                        break
        with open(chemin + '/data/samedi_ferie.pic','rb') as file:
            pic=pickle.Unpickler(file)
            self.saturday = pic.load()
            self.feria = pic.load()
            
        return tuple(tmp)
    
    def put_in_year(self, year):
        """A method which puts feasts in the year"""
        easter = self.easter(year)
        for raw_elt in self.raw_data:
            elt = raw_elt.copy()
            if isinstance(elt.DateCivile(easter,year),datetime.date): #TODO faire de toutes ces fonctions des méthodes
                date=elt.DateCivile(easter,year)
                self.move(elt,date)
            else:
                for a in elt.DateCivile(easter,year):
                    self.move(a,a.date)
        
    def create_year(self,year):
        """A function which emules the liturgical 'year' requested.
        Add year in self.year_names.
        Create a year in self.year_data."""
        self.year_names.append(year)
        self.year_names.sort()
        
        if year not in self.previous_year_names and year not in self.next_year_names:
            self.year_data[year] = self.create_empty_year(year)
            self.put_in_year(year)
        elif year in self.previous_year_names:
            self.previous_year_names.remove(year)
            self.year_data[year] = self.previous_year_data.pop(year)
        else:
            self.next_year_names.remove(year)
            self.year_data[year] = self.next_year_data.pop(year)
            self.put_in_year(year)
            
        pyear = year - 1
        if pyear not in self.year_names:
            self.previous_year_names.append(pyear)
            self.previous_year_names.sort()
            self.previous_year_data[pyear] = self.create_empty_year(pyear)
            self.put_in_year(pyear)
        
        date = datetime.date(year,1,1)
        for month in self.year_data[year]:
            for day in month:
                self.selection(day,date)
                date += datetime.timedelta(1)
        
        
    def create_empty_year(self,year):
        """A method which creates the skeleton of each year"""
        tmp = list()
        for i in range(12):
            if i in (3,5,8,10):
                j = 30
            elif i == 1:
                if calendar.isleap(year):
                    j = 29
                else:
                    j = 28
            else:
                j = 31
            tmp.append([ [] for i in range(j)])
        return tmp
    
    def __call__(self,first,last=None):
        if not last:
            last = first + 1
        else:
            last += 1
        for year in range(first,last):
            if year not in self.year_names:
                self.create_year(year)
        
    def __getitem__(self, request): # WARNING comportement incohérent : supprimer la 'magie'
        """A method to process request like LiturgicalYear[1962].
        It accepts two types of request :
        - years
        - datetime.date
        If requested year is not yet loaded,
        it is automatically loaded and returned."""
        if isinstance(request,int):
            if request not in self.year_names:
                self.create_year(request)
            return self.year_data[request]
        elif isinstance(request, datetime.date):
            if request.year in self.previous_year_names: # il faut donc vérifier l'existence de la date auparavant
                return self.previous_year_data[request.year][request.month - 1][request.day - 1]
            elif request.year not in self.year_names: # peu satisfaisant : il faudrait une demande explicite (avec __call__ ?)
                self.create_year(request.year)
            return self.year_data[request.year][request.month - 1][request.day - 1]
        elif isinstance(request,slice): # TODO tenir compte du step
            answer = []
            for day in self:
                if day[0].date >= request.start and day[0].date <= request.stop:
                    answer.append(day)
            return answer
        
    def __setitem__(self,key,value):
        """A method to process request like LiturgicalYear[datetime.date(2010,1,1] = []"""
        if key.year in self.previous_year_names:
            self.previous_year_data[key.year][key.month - 1][key.day - 1] = value
        elif key.year not in self.year_names:
            self.next_year_names.append(key.year)
            self.next_year_data[key.year] = self.create_empty_year(year)
            #self.create_year(key.year) # WARNING cela peut causer des boucles infinies : il vaut mieux créer une année vide.
        else:
            self.year_data[key.year][key.month - 1][key.day - 1] = value
            
    def __contains__(self,value):
        """This method determines wether a year exists as a complete year"""
        if isinstance(value,datetime.date):
            value = value.year
        if value in self.year_data:
            return True
        else:
            return False
        
    def __len__(self):
        """Returns number of years loaded"""
        return len(self.year_names)
    
    def __iter__(self):
        """Iters from the first day of January of the first year
        until the 31th of December of the last year.
        Yield a list containing feasts of the day."""
        for year in self.year_names:
            for month in self.year_data[year]:
                for day in month:
                    yield day
    def __repr__(self):
        return """LiturgicalYear. {}/{}""".format(self.ordo,self.proper)
    
    def __str__(self):
        return """LiturgicalYear. Ordo : {}. Proper : {}. Years already loaded : {}.""".format(self.ordo,self.proper,', '.join([ str(year) for year in self.year_names]))
    
    def easter(self,year):
        """Return a datetime.date object with the Easter date of the year. The function is only available between 1583 and 4100.
        I didn't write this function, but I found it here : http://python.jpvweb.com/mesrecettespython/doku.php?id=date_de_paques """
        a=year//100
        b=year%100
        c=(3*(a+25))//4
        d=(3*(a+25))%4
        e=(8*(a+11))//25
        f=(5*a+b)%19
        g=(19*f+c-e)%30
        h=(f+11*g)//319
        j=(60*(5-d)+b)//4
        k=(60*(5-d)+b)%4
        m=(2*j-k-g+h)%7
        n=(g-h+m+114)//31
        p=(g-h+m+114)%31
        day=p+1
        month=n
        return datetime.date(year,month,day)
    
    def trouve(self,entre,cherche,liste=latinus):
        """Returns a boolean. Find if the propre 'entre' matches whith the propre 'cherche' in the 'liste'."""
        if entre == cherche:
            return True
        else:
            sortie=entre
            while sortie != 'latinus':
                sortie=self.remonte(liste, sortie)
                if sortie == cherche:
                    return True
        return False
    
    def remonte(self,liste, entre, nom='latinus'):
        """Function used in the 'trouve' function. Find the proper which is before the 'entre' one in the 'liste'."""
        if entre in liste.keys():
            entre=nom
            return nom
        for a in liste.keys():
            entre=self.remonte(liste[a],entre,a)
        return entre
    
    def weekmonth(self,year,month,week):
        """Return a list a feasts for requested week of 'month' in 'year'.
        Weeks starts with Sundays and may be incomplete.
        Week number start with 0."""
        week_list = liturgiccal.monthdayscalendar(year,month)[week]
        return [ self[datetime.date(year,month,day)] for day in week_list if day != 0]
        
    def move(self,new_comer,date):
        """Move 'new_comer' if necessary, and put it at the right date.
        new_comer: a Fete class ;
        date: a datetime.date ;
        """
        if self[date] == []:
            self[date].append(new_comer)
            return self
        
        #Faut-il déplacer ?
        opponent = self[date][0]

        # Cas de 'new_comer' ayant la même self.personne que 'opponent'
        if new_comer.personne == opponent.personne:
            self[date].append(new_comer)
        # Cas de 'new_comer' et 'opponent' tous deux transférés
        elif new_comer.transferee and opponent.transferee:
            if new_comer.priorite > opponent.priorite:
                self[date][0] = new_comer
                opponent.transferee=True
                self.move(opponent,date + datetime.timedelta(1))
            else:
                new_comer.date = new_comer.date + datetime.timedelta(1)
                self.move(new_comer,date + datetime.timedelta(1))
        # Si l'un ou l'autre est transféré
        elif new_comer.transferee and opponent.priorite > 800:
            new_comer.date = new_comer.date + datetime.timedelta(1)
            self.move(new_comer,date + datetime.timedelta(1))
        elif opponent.transferee and new_comer.priorite > 800:
            self[date][0] = new_comer
            opponent.date = opponent.date + datetime.timedelta(1)
            self.move(opponent,date + datetime.timedelta(1))
        # Cas de 'new_comer' fête de première classe vs 'opponent' fête de première classe
        elif new_comer.priorite > 1600:
            if new_comer.priorite < opponent.priorite and not new_comer.dimanche:
                new_comer.transferee=True
                self.move(new_comer,date + datetime.timedelta(1))
            elif opponent.priorite > 1600 and opponent.priorite < new_comer.priorite and not opponent.dimanche:
                self[date][0] = new_comer
                opponent.transferee=True
                self.move(opponent,date + datetime.timedelta(1))
            else:
                self[date].append(new_comer)
        elif self.proper != 'romanus' and (new_comer.occurrence_perpetuelle or opponent.occurrence_perpetuelle):
            premier_dimanche_avent = dimancheapres(datetime.date(year,12,25)) - datetime.timedelta(28)
            # Cas de 'new_comer' fête de seconde classe empêchée perpétuellement # WARNING pourquoi la valeur self.transferee n'est-elle pas modifiée en-dessous ? WARNING
            if new_comer.priorite > 800 and opponent.priorite > 800 and opponent.priorite > new_comer.priorite and not new_comer.dimanche:
                new_comer.date = new_comer.date + datetime.timedelta(1)
                self.move(new_comer, date + datetime.timedelta(1))
            elif opponent.priorite > 800 and new_comer.priorite > 800 and new_comer.priorite > opponent.priorite and not opponent.dimanche:
                self[date][0] = new_comer
                opponent.date = opponent.date + datetime.timedelta(1)
                self.move(opponent,date + datetime.timedelta(1))
            # Cas de 'new_comer' fête de troisième classe particulière empêchée perpétuellement 
            elif not date - paques >= datetime.timedelta(-46) and not date - paques < datetime.timedelta(0) and not new_comer.date < datetime.date(year,12,25) and not new_comer.date >= premier_dimanche_avent:
                if new_comer.priorite <= 700 and new_comer.priorite >= 550 and new_comer.priorite < opponent.priorite and not new_comer.dimanche:
                    new_comer.date = new_comer.date + datetime.timedelta(1)
                    self.move(new_comer, date + datetime.timedelta(1))
                elif opponent.priorite <=700 and new_comer.priorite >= 550 and new_comer.priorite > opponent.priorite and not opponent.dimanche:
                    self[date][0] = new_comer
                    opponent.date = opponent.date + datetime.timedelta(1)
                    self.move(opponent,date + datetime.timedelta(1))
                else:
                    self[date].append(new_comer)
        else:
            self[date].append(new_comer)
        self[date].sort(key=lambda x: x.priorite,reverse=True)
        
    def selection(self,liste,date): #DEPRECATED
        """Selects the feasts which are actually celebrated."""
        
        commemoraison = 0 # max 2
        commemoraison_temporal=False
        
        if len(liste) == 0 or liste[0].degre == 5:
            self.saturday.date = date
            if self.saturday.Est_ce_samedi(date):
                liste.append(self.saturday.copy())
            else:
                liste.append(self.feria.Dimanche_precedent(date,self))
            
        liste.sort(key=lambda x: x.priorite,reverse=True)
        
        liste[0].commemoraison = False
        liste[0].omission = False
        liste[0].celebree=True
        i="nothing, it's just for the joke. How funny I am !"
        tmp = liste[0]
        liste = sorted(liste[1:], key=lambda a: a.commemoraison_privilegiee, reverse=True)
        
        if tmp.dimanche or tmp.fete_du_Seigneur and datetime.date.isoweekday(date) == 7:
            for hideux, elt in enumerate(liste):
                liste[hideux].omission = True
                liste[hideux].celebree = False
        elif tmp.priorite >= 1650:
            for hideux,elt in enumerate(liste):
                liste[hideux].celebree=False
                if elt.personne == tmp.personne:
                    liste[hideux].omission = True
                    liste[hideux].celebree = False
                elif elt.commemoraison_privilegiee > 0 and commemoraison == 0 and not (tmp.fete_du_Seigneur and elt.dimanche or tmp.dimanche and elt.fete_du_Seigneur):
                    liste[hideux].commemoraison=True
                    commemoraison = 1
                else:
                    liste[hideux].commemoraison=False
                    liste[hideux].omission=True
                    
        elif tmp.priorite >= 900:
            for hideux,elt in enumerate(liste):
                liste[hideux].celebree=False
                if elt.personne == tmp.personne:
                    liste[hideux].omission = True
                    liste[hideux].celebree = False
                elif commemoraison == 0 and elt.degre >= 2 and not (tmp.fete_du_Seigneur and elt.dimanche or tmp.dimanche and elt.fete_du_Seigneur):
                    liste[hideux].commemoraison=True
                    commemoraison = 1
                else:
                    liste[hideux].commemoraison=False
                    liste[hideux].omission=True
                    
        elif tmp.priorite >= 400:
            for hideux,elt in enumerate(liste):
                liste[hideux].celebree=False
                if elt.personne == tmp.personne:
                    liste[hideux].omission = True
                    liste[hideux].celebree = False
                elif commemoraison <= 2 and not commemoraison_temporal:
                    liste[hideux].commemoraison=True
                    commemoraison_temporal=liste[hideux].temporal
                    commemoraison += 1
                else:
                    liste[hideux].commemoraison=False
                    liste[hideux].omission=True
        
        elif tmp.priorite >= 200:
            tmp.celebree=False
            tmp.peut_etre_celebree=True
            for hideux,elt in enumerate(liste):
                liste[hideux].celebree=False
                liste[hideux].peut_etre_celebree=True
                if elt.personne == tmp.personne:
                    liste[hideux].omission = True
                elif commemoraison <= 2 and not commemoraison_temporal:
                    liste[hideux].commemoraison=True
                    commemoraison_temporal=liste[hideux].temporal
                    commemoraison += 1
                else:
                    liste[hideux].commemoraison=False
                    liste[hideux].omission=True
        
        liste = [tmp] + liste
        liste.sort(key=lambda x: x.priorite,reverse=True) # useless ?
        
        self[date] = liste
