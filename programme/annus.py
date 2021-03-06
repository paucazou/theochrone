#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import calendar
import datetime
import officia # not really useful; just to compute sunday before
import os
import pickle

chemin = os.path.dirname(os.path.abspath(__file__))

fichiers=('roman_1962_.pkl',
        'australian_1962_.pkl',
        'american_1962_.pkl',
        'brazilian_1962_.pkl',
        'canadian_1962_.pkl',
        'english_1962_.pkl',
        'french_1962_.pkl',
        'newzealander_1962_.pkl', 
        'polish_1962_.pkl',
        'portuguese_1962_.pkl',
        'scottish_1962_.pkl',
        'strasburger_1962_.pkl',
        'welsh_1962_.pkl',
        )
""""
    'romanus_1962_dimanches.pic', 
    'romanus_1962_fetesduseigneur.pic',
    'romanus_1962_cycledenoel.pic',
    'romanus_1962_cycledepaques.pic',
    'romanus_1962_premiertrimestre_sanctoral.pic',
    'romanus_1962_deuxiemetrimestre_sanctoral.pic',
    'romanus_1962_troisiemetrimestre_sanctoral.pic',
    'romanus_1962_quatriemetrimestre_sanctoral.pic',
    #'gallicanus_1962_dimanches.pic',""" # DEPRECATED
    

latin={
    'roman':{
        'australian':{},
        'american': {},
        'brazilian': {},
        'canadian': {},
        'english': {},
        'french':{
            'strasburger':{},
            },
        'newzealander':{},
        'polish': {},
        'portuguese' : {},
        'scottish': {},
        'spanish': {},
        'welsh': {},

        'italian':{},
        'testis':{}, # a test proper, only used with the --test arg.
        },
        'dominicanus':{}, # TODO translate them in english
        'cartusiensis': {},
        'visigothica':{},
        'ambrosianus':{},
        'cisterciensis':{},
        'bracarenses':{},
        } # contains the pyramid of the propers ; used in the 'remonte' and 'trouve' functions 
        
liturgiccal=calendar.Calendar(firstweekday=6)

# Functions

def oncecalled(function):
    """Decorator which checks wether the function was called or not"""
    def _oncecalled(*args,**kwargs):
        self=args[0]
        if hash(function) in self.once_called:
            return False
        else:
            self.once_called.append(hash(function))
            return function(*args,**kwargs)
    return _oncecalled

# class

class LiturgicalCalendar():
    """This class is a collection which contains the whole
    liturgical years requested during the time of the program.
    Functions started with _ should not be accessed
    from outside the class"""
    instances = []
    propers_ordo = [(name.split('_')[0],int(name.split('_')[1])) for name in fichiers]

    def __new__(cls,proper='roman',ordo=1962):
        """Checks if an instance of the requested calendar
        has been already loaded.
        return a loaded instance, or a new one."""
        if (proper,ordo) not in cls.propers_ordo: # check parameters correctness
            proper='roman'
            ordo=1962
        instance_loaded = [elt for elt in cls.instances if elt.proper == proper and elt.ordo == ordo]
        if instance_loaded:
            return instance_loaded[0]
        return object.__new__(cls)
    
    def __init__(self, proper='roman',ordo=1962):
        """Init of the instance"""
        if self in type(self).instances: # if the instance already exists, does nothing
            return
        self.once_called = [] # A list containing hash of methods once called
        self._load_raw_data(proper,ordo) # tuple which contains the data extracted from files
        self.year_names = [] # an ordered list of the year currently saved in the instance
        self.year_data = {} # a dict which contains the liturgical years themselves.
        
        self.previous_year_names = []
        self.previous_year_data = {}
        self.next_year_names = []
        self.next_year_data = {}
        
        self.ordo = ordo
        self.proper = proper
        type(self).instances.append(self)
                
     
    @oncecalled
    def _load_raw_data(self,proper,ordo): # TEST
        """Method used only when creating the instance.
        It loads raw data following the 'proper' and the 'ordo' requested.
        Returns a tuple whith the whole data"""
        self.raw_data = []
        for fichier in [file for file in fichiers if file.split('_')[1] == str(ordo) and self.trouve(proper,file.split('_')[0])]:
            with open(chemin + '/data/' + fichier, 'rb') as file:
                pic=pickle.Unpickler(file)
                self.raw_data += pic.load()
                if 'roman' in fichier:
                    *self.raw_data,self.saturday,self.feria = self.raw_data # TODO trouver un moyen plus sûr de faire passer la férie et le samedi 
        
        # managing feasts which have also a Pro Aliquibus Locis mass
        other_pal = []
        for elt in self.raw_data:
            if elt.pal and elt.priorite > 50:
                # managing pal mass
                pal_elt = elt.copy()
                pal_elt._priorite, pal_elt.degre = 50, 6
                pal_elt.temporal = pal_elt.sanctoral = False
                pal_elt.link = pal_elt.pal_link
                # setting pal of elt to False
                elt.pal = False
                
                other_pal.append(pal_elt)
        # add pal masses to self.raw_data
        self.raw_data.extend(other_pal)
        
        """with open(chemin + '/data/samedi_ferie.pic','rb') as file:
            pic=pickle.Unpickler(file)
            self.saturday, self.feria = pic.load()    """    
    
    def _put_in_year(self, year): # TEST
        """A method which puts feasts in the year"""
        easter = self.easter(year)
        for raw_elt in self.raw_data:
            elt = raw_elt.copy()
            if isinstance(elt.DateCivile(easter,year),datetime.date):
                date=elt.DateCivile(easter,year)
                elt.parent = self
                self._move(elt,date)
            else:
                if elt.DateCivile(easter,year) is None: import pdb;pdb.set_trace()
                for a in elt.DateCivile(easter,year):
                    a.parent = self
                    self._move(a,a.date)
        
    def _create_year(self,year): # TEST
        """A function which emulates the liturgical 'year' requested.
        Add year in self.year_names.
        Create a year in self.year_data."""
        self.year_names.append(year)
        self.year_names.sort()
        
        if year not in self.previous_year_names and year not in self.next_year_names:
            self.year_data[year] = self.create_empty_year(year)
            self._put_in_year(year)
        elif year in self.previous_year_names:
            self.previous_year_names.remove(year)
            self.year_data[year] = self.previous_year_data.pop(year)
        else:
            self.next_year_names.remove(year)
            self.year_data[year] = self.next_year_data.pop(year)
            self._put_in_year(year)
            
        pyear = year - 1
        if pyear not in self.year_names:
            self.previous_year_names.append(pyear)
            self.previous_year_names.sort()
            if pyear in self.next_year_names:
                self.next_year_names.remove(pyear)
                self.previous_year_data[pyear] = self.next_year_data.pop(pyear)
            else:
                self.previous_year_data[pyear] = self.create_empty_year(pyear)
            self._put_in_year(pyear)
        
        date = datetime.date(year,1,1)
        for date, day in self.year_data[year].items():
            self._selection(day,date)
        
    
    @staticmethod
    def create_empty_year(year): #TEST
        """A method which creates the skeleton of each year"""
        tmp = {}
        date=datetime.date(year,1,1)
        while date.year == year:
            tmp[date] = []
            date += datetime.timedelta(1)
        return tmp
    
    def __call__(self,first,last=None): #TEST
        if not last:
            last = first + 1
        else:
            last += 1
        if first > last or first < 1600 or last > 4100:
            return False
        for year in range(first,last):
            if year not in self.year_names:
                self._create_year(year)
        
    def __getitem__(self, request): # TEST
        """A method to process request like LiturgicalYear[1962].
        It accepts two types of request :
        - years
        - datetime.date
        If requested year is not yet loaded,
        it is automatically loaded and returned."""
        if isinstance(request,int):
            return self.year_data[request]
        elif isinstance(request, datetime.date):
            return self.year_data[request.year][request]
        elif isinstance(request,slice): # TODO tenir compte du step
            answer = []
            for day in self.__iter__():
                if day[0].date >= request.start and day[0].date <= request.stop:
                    answer.append(day)
            return answer
        
    def __setitem__(self,key,value): #TEST
        """A method to process request like LiturgicalYear[datetime.date(2010,1,1)] = []"""
        if key.year in self.previous_year_names:
            self.previous_year_data[key.year][key] = value
        elif key.year not in self.year_names:
            self.next_year_names.append(key.year)
            self.next_year_data[key.year] = self.create_empty_year(key.year)
            self.next_year_data[key.year][key] = value
        else:
            self.year_data[key.year][key] = value
            
    def __contains__(self,value): #TEST
        """This method determines wether a year exists as a complete year"""
        if isinstance(value,datetime.date):
            value = value.year
        if value in self.year_data:
            return True
        else:
            return False
        
    def __len__(self): #TEST
        """Returns number of years loaded"""
        return len(self.year_names)
    
    def __iter__(self): #TEST
        """Iters from the first day of January of the first year
        until the 31th of December of the last year.
        Yield a list containing feasts of the day."""
        for year in self.year_names:
            for date,day in sorted(self.year_data[year].items()):
                yield day
                
    def __repr__(self): #TEST
        return """LiturgicalYear. {}/{}""".format(self.ordo,self.proper)
    
    def __str__(self): #TEST
        return """LiturgicalYear. Ordo : {}. Proper : {}. Years already loaded : {}.""".format(self.ordo,self.proper,', '.join([ str(year) for year in self.year_names]))
    
    @staticmethod
    def easter(year): #TEST # TODO maybe save the dates found in a list and return this value if requested twice or more
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
    
    @classmethod
    def trouve(cls,entre,cherche,liste=latin): # TEST
        """Returns a boolean. Find if the propre 'entre' matches whith the propre 'cherche' in the 'liste'."""
        if entre == cherche:
            return True
        else:
            sortie=entre
            while sortie != 'latin':
                sortie=cls.remonte(liste, sortie)
                if sortie == cherche:
                    return True
        return False
    
    @classmethod
    def remonte(cls,liste, entre, nom='latin'): #TEST
        """Function used in the 'trouve' function. Find the proper which is before the 'entre' one in the 'liste'."""
        if entre in liste.keys():
            entre=nom
            return nom
        for a in liste.keys():
            entre=cls.remonte(liste[a],entre,a)
        return entre
    
    def unsafe_get(self,date): #TEST # TODO make a class views ?
        """Return a list of feasts if 'date' exists in self.year_data.
        If not, tries to return from self.previous_year_data
        or self.next_year_data, else False"""
        if date.year in self.year_names:
            return self.year_data[date.year][date]
        elif date.year in self.previous_year_names:
            retour = self.previous_year_data[date.year][date]
            return retour if retour != [] else False
        elif date.year in self.next_year_names:
            retour = self.next_year_data[date.year][date]
            return retour if retour != [] else False
        else:
            return False
        
    def unsafe_iter(self,start=None,stop=None,reverse=False): #TEST
        """Iterator which uses self.unsafe_get function
        to yield items.
        start and stop are datetime.date objects.
        reverse is a bool.
        If reverse is used, stop and start are reversed. # UNCLEAR
        """
        
        if not start:
            start = datetime.date(sorted(self.year_names + self.previous_year_names + self.next_year_names)[0],1,1)
        if not stop:
            stop = datetime.date(sorted(self.year_names + self.previous_year_names + self.next_year_names)[-1],12,31)
        if not reverse:
            step = 1
            date = start
            stop = stop + datetime.timedelta(1)
        else:
            step = -1
            date = stop
            stop = start - datetime.timedelta(1)
        while date != stop:
            yield self.unsafe_get(date)
            date = date + datetime.timedelta(step)
            
    
    def weekmonth(self,year,month,week,debut=0,fin=32): #TEST
        """Return a list a feasts for requested week of 'month' in 'year'.
        Weeks starts with Sundays and may be incomplete.
        Week number start with 0."""
        try:
            week_list = liturgiccal.monthdayscalendar(year,month)[week]
        except IndexError:
            return False
        return { datetime.date(year,month,day) : self.year_data[year][datetime.date(year,month,day)]
                for day in week_list if day != 0 and day >= debut and day <= fin }
    
    def listed_month(self,year,month,debut=0,fin=32): # TEST
        """Return a list of weeks for requested month of year.
        January = 1"""
        month_dic = {}
        for i in range(7):
            week = self.weekmonth(year,month,i,debut,fin)
            if week == {}:
                continue
            elif not week:
                break
            month_dic[(i,'week')] = week
        return month_dic
    
    def listed_year(self,year,debut=None,fin=None): # TEST
        """Return a dic of months for requested year.
        'debut' and 'fin' are datetime.date of the requested 'year'."""
        if not debut:
            debut = datetime.date(year,1,1)
        if not fin:
            fin = datetime.date(year,12,31)
        year_list = {}
        for i in range(1,13):
            if i == debut.month and i == fin.month:
                year_list[(i,'month')] = self.listed_month(year,i,debut.day,fin.day)
            elif i  == debut.month:
                year_list[(i,'month')] = self.listed_month(year,i,debut=debut.day)
            elif i == fin.month:
                year_list[(i,'month')] = self.listed_month(year,i,fin=fin.day)
            elif i > debut.month and i < fin.month:
                year_list[(i,'month')] = self.listed_month(year,i)
        return year_list
    
    def listed_arbitrary(self,debut,fin): #TEST
        """Returns an arbitrary span listed by week, month and year, if necessary"""
        weeknumber = lambda x : [i for i, week in enumerate(liturgiccal.monthdayscalendar(x.year,x.month)) if x.day in week][0]
        if weeknumber(debut) == weeknumber(fin) and debut.month == fin.month and debut.year == fin.year:
            return self.weekmonth(debut.year,debut.month,
                                  weeknumber(debut),debut.day,fin.day)
        elif debut.month == fin.month and debut.year == fin.year:
            return self.listed_month(debut.year,debut.month,
                                     debut.day,fin.day)
        elif debut.year == fin.year:
            return self.listed_year(debut.year,debut,fin)
        else:
            retour = {}
            for year in range(debut.year,fin.year + 1):
                if debut.year == year :
                    retour[year] = self.listed_year(year,debut=debut)
                elif fin.year == year :
                    retour[year] = self.listed_year(year,fin=fin)
                else:
                    retour[year] = self.listed_year(year)
            return retour
    
    def liturgicalYear(self,year):
        """Return the whole liturgical year for specified year
        dict(date:[feast,feast,...])"""
        self.__call__(year-1,year)
        limits = []
        for i in range(year-1,year+1):
            for day in self.unsafe_iter(datetime.date(i,11,21),datetime.date(i,12,8)):
                for feast in day:
                    if feast.nom['en'] == 'First Sunday of Advent':
                        limits.append(feast.date)
                        break
        limits[1] = limits[1] - datetime.timedelta(1)
        return self.unsafe_iter(*limits)
    
    def isdayinlyear(self,day,year):
        """Return True if day is in liturgical year"""
        return True if day in ( elt[0].date for elt in self.liturgicalYear(year)) else False            
    
    def _move(self,new_comer,date): #TEST
        """Move 'new_comer' if necessary, and put it at the right date.
        new_comer: a Fete class ;
        date: a datetime.date ;
        """
        easter = self.easter(date.year)
        if date.year in self.year_names:
            liste = self.year_data[date.year][date]
        elif date.year in self.previous_year_names:
            liste = self.previous_year_data[date.year][date]
        else:
            if date.year not in self.next_year_names:
                self.next_year_names.append(date.year)
                self.next_year_data[date.year] = self.create_empty_year(date.year)
            liste = self.next_year_data[date.year][date]
        
        if liste == []:
            liste.append(new_comer)
            return
        
        #Faut-il déplacer ?
        opponent = liste[0]
        
        # Case of a new_comer.pal == True -> Pro Aliquibus Locis
        if new_comer.pal: # NOT TESTED
            liste.append(new_comer)
        # Cas de 'new_comer' ayant la même self.personne que 'opponent'
        elif new_comer.personne.intersection(opponent.personne):
            liste.append(new_comer)
        # Cas de 'new_comer' et 'opponent' tous deux transférés
        elif new_comer.transferee and opponent.transferee:
            if new_comer.priorite > opponent.priorite:
                liste[0] = new_comer
                opponent.transferee=True
                self._move(opponent,date + datetime.timedelta(1))
            else:
                new_comer.date = new_comer.date + datetime.timedelta(1)
                self._move(new_comer,date + datetime.timedelta(1))
        # Si l'un ou l'autre est transféré
        elif new_comer.transferee and opponent.priorite > 800:
            new_comer.date = new_comer.date + datetime.timedelta(1)
            self._move(new_comer,date + datetime.timedelta(1))
        elif opponent.transferee and new_comer.priorite > 800:
            liste[0] = new_comer
            opponent.date = opponent.date + datetime.timedelta(1)
            self._move(opponent,date + datetime.timedelta(1))
        # Cas de 'new_comer' fête de première classe vs 'opponent' fête de première classe
        elif new_comer.priorite > 1600:
            if new_comer.priorite < opponent.priorite and not new_comer.dimanche:
                new_comer.transferee=True
                self._move(new_comer,date + datetime.timedelta(1))
            elif opponent.priorite > 1600 and opponent.priorite < new_comer.priorite and not opponent.dimanche:
                liste[0] = new_comer
                opponent.transferee=True
                self._move(opponent,date + datetime.timedelta(1))
            else:
                liste.append(new_comer)
        elif self.proper != 'roman' and (new_comer.occurrence_perpetuelle or opponent.occurrence_perpetuelle):
            premier_dimanche_avent = officia.dimancheapres(datetime.date(date.year,12,25)) - datetime.timedelta(28)
            # Cas de 'new_comer' fête de seconde classe empêchée perpétuellement # WARNING pourquoi la valeur self.transferee n'est-elle pas modifiée en-dessous ? WARNING
            if new_comer.priorite > 800 and opponent.priorite > 800 and opponent.priorite > new_comer.priorite and not new_comer.dimanche:
                new_comer.date = new_comer.date + datetime.timedelta(1)
                self._move(new_comer, date + datetime.timedelta(1))
            elif opponent.priorite > 800 and new_comer.priorite > 800 and new_comer.priorite > opponent.priorite and not opponent.dimanche:
                liste[0] = new_comer
                opponent.date = opponent.date + datetime.timedelta(1)
                self._move(opponent,date + datetime.timedelta(1))
            # Cas de 'new_comer' fête de troisième classe particulière empêchée perpétuellement 
            elif not date - easter >= datetime.timedelta(-46) and not date - easter < datetime.timedelta(0) and not new_comer.date < datetime.date(date.year,12,25) and not new_comer.date >= premier_dimanche_avent:
                if new_comer.priorite <= 700 and new_comer.priorite >= 550 and new_comer.priorite < opponent.priorite and not new_comer.dimanche:
                    new_comer.date = new_comer.date + datetime.timedelta(1)
                    self._move(new_comer, date + datetime.timedelta(1))
                elif opponent.priorite <=700 and new_comer.priorite >= 550 and new_comer.priorite > opponent.priorite and not opponent.dimanche:
                    liste[0] = new_comer
                    opponent.date = opponent.date + datetime.timedelta(1)
                    self._move(opponent,date + datetime.timedelta(1))
                else:
                    liste.append(new_comer)
            else:
                liste.append(new_comer)
        else:
            liste.append(new_comer)
        liste.sort(key=lambda x: x.priorite,reverse=True)
        
    def _selection(self,liste,date): # TEST 
        """Selects the feasts which are actually celebrated."""
        
        commemoraison = 0 # max 2
        commemoraison_temporal=False
        
        if len(liste) == 0 or liste[0].priorite <= 110:
            self.saturday.date = date
            if self.saturday.Est_ce_samedi(date):
                liste.append(self.saturday.copy())
                liste[-1].parent = self
            else:
                liste.append(self.feria.CreateFeria(date,self))
            
        liste.sort(key=lambda x: x.priorite,reverse=True)
        
        liste[0].commemoraison = False
        liste[0].omission = False
        liste[0].celebree=True
        i="nothing, it's just for the joke. How funny I am !"
        tmp = liste[0]
        liste = sorted(liste[1:], key=lambda a: a.commemoraison_privilegiee, reverse=True)
        
        if tmp.dimanche or tmp.fete_du_Seigneur and datetime.date.isoweekday(date) == 7:
            if 1650 > tmp.priorite >= 900:
                for hideux, elt in enumerate(liste):
                    if not tmp.personne.intersection(elt.personne) and (elt.commemoraison_privilegiee > 0 or 1650 > elt.priorite >= 900) and commemoraison < 1 and elt.dimanche == False and elt.fete_du_Seigneur == False:
                        commemoraison += 1
                        liste[hideux].celebree = False
                        liste[hideux].omission = False
                        liste[hideux].commemoraison = True
                    else:
                        liste[hideux].omission = True
                        liste[hideux].celebree = False
            else:
                for hideux, elt in enumerate(liste):
                    liste[hideux].omission = True
                    liste[hideux].celebree = False
        elif tmp.priorite >= 1650:
            for hideux,elt in enumerate(liste):
                liste[hideux].celebree=False
                if elt.pal:
                    liste[hideux].omission = True
                elif elt.personne.intersection(tmp.personne):
                    liste[hideux].omission = True
                elif elt.commemoraison_privilegiee > 0 and commemoraison == 0:
                    liste[hideux].commemoraison=True
                    commemoraison = 1
                else:
                    liste[hideux].commemoraison=False
                    liste[hideux].omission=True
                    
        elif tmp.priorite >= 900:
            for hideux,elt in enumerate(liste):
                liste[hideux].celebree=False
                if elt.pal:
                    liste[hideux].omission = True
                elif elt.personne.intersection(tmp.personne):
                    liste[hideux].omission = True
                    liste[hideux].celebree = False
                elif commemoraison == 0:
                    liste[hideux].commemoraison=True
                    commemoraison = 1
                else:
                    liste[hideux].commemoraison=False
                    liste[hideux].omission=True
                    
        elif tmp.priorite >= 400:
            for hideux,elt in enumerate(liste):
                liste[hideux].celebree=False
                if elt.pal and elt.personne.intersection(tmp.personne):
                    elt.peut_etre_celebree = True
                    elt.omission = False
                elif elt.personne.intersection(tmp.personne):
                    liste[hideux].omission = True
                    liste[hideux].celebree = False
                elif commemoraison < 2 and (elt.sanctoral or (elt.temporal and commemoraison_temporal == False)):
                    liste[hideux].commemoraison=True
                    commemoraison_temporal=liste[hideux].temporal
                    commemoraison += 1
                    
                else:
                    #print(elt.nom)
                    liste[hideux].commemoraison=False
                    liste[hideux].omission=True
        
        elif tmp.priorite >= 200:
            tmp.celebree=False
            tmp.peut_etre_celebree=True
            for hideux,elt in enumerate(liste):
                liste[hideux].celebree=False
                liste[hideux].peut_etre_celebree=True
                if elt.pal:
                    liste[hideux].peut_etre_celebree = True
                    liste[hideux].omission = False
                elif elt.personne.intersection(tmp.personne):
                    liste[hideux].omission = True
                    liste[hideux].peut_etre_celebree = False
                elif commemoraison < 2 and (elt.sanctoral or (elt.temporal and commemoraison_temporal == False)):
                    liste[hideux].commemoraison=True
                    commemoraison_temporal=liste[hideux].temporal
                    commemoraison += 1
                else:
                    liste[hideux].commemoraison=False
                    liste[hideux].omission=True
        
        liste = [tmp] + liste
        liste.sort(key=lambda x: x.priorite,reverse=True)
        
        self.year_data[date.year][date] = liste
