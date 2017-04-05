#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import easter_dates
import datetime
import dossier
import os
import pytest
import random
import subprocess
import unittest.mock as mock

dossier.main()
import annus

class FakeFeast(mock.MagicMock):
    """A class which simulates the Fete class behaviour"""
    personne_list = [1]
    
    def __init__(self,
                 nom=None,
                 degre=1,priorite=1,commemoraison_privilegiee=90,
                 date=(1,1),personne=None,
                 dimanche=False,fete_du_Seigneur=False,):
        mock.MagicMock.__init__(self)
        self.priorite = priorite
        self.degre = degre
        self.commemoraison_privilegiee = commemoraison_privilegiee
        self.date = None
        self.date_ = date
        if not personne:
            self.personne = str(FakeFeast.personne_list[-1]) + str(random.randrange(500))
        else:
            self.personne = personne
        FakeFeast.personne_list.append(self.personne)
        
        if not nom:
            self.nom = """FakeFeast d:{},p:{},c:{},D:{},P:{}""".format(
                self.degre,self.priorite,self.commemoraison_privilegiee,
                self.date,self.personne)
        else:
            self.nom = nom
        
        self.dimanche = dimanche
        self.fete_du_Seigneur = fete_du_Seigneur
        
        self.peut_etre_celebree=False
        self.transferee=False
        self.date_originelle=None
        self.celebree=True
        self.omission=False
        self.commemoraison=False
        
        self.proper = 'romanus'
        self.ordo = 1962
        
    def __repr__(self):
        return self.nom
        
    def DateCivile(self,easter,year):
        self.date = datetime.date(year,self.date_[0],self.date_[1])
        return self.date
    
    def copy(self):
        new = self.__class__()
        new.__dict__ = self.__dict__.copy()
        return new
    
class FakeFeast_with_DateCivile_as_iterable(FakeFeast):
    def DateCivile(self,easter,year):
        return FakeFeast('FromIterable1'),FakeFeast('FromIterable2')


def FakeFeast_basic_iterator(year=1962):
    date=datetime.date(year,1,1)
    while True:
        yielded=FakeFeast(date=(date.month,date.day))
        yield yielded
        date = date + datetime.timedelta(1)
        if date.year != year:
            break

@mock.patch("pickle.Unpickler")
@mock.patch("__main__.open")
@pytest.fixture
def send_empty_liturgical_calendar(mock_open,mock_unpickler):
    mock_load = mock.MagicMock()
    mock_load.load.return_value=[mock.MagicMock(),mock.MagicMock()]
    mock_unpickler.return_value = mock_load
    return annus.LiturgicalCalendar()

@pytest.fixture
def send_one_year_liturgical_calendar(send_empty_liturgical_calendar):
    L = send_empty_liturgical_calendar
    L(1962)
    return L

def test_paques():
    """A function to test every easter date from 1600 to 4100"""
    for year in range(1600,4100):
        assert annus.LiturgicalCalendar.easter(year) == easter_dates.check_dates[year]
        
def test_oncecalled():
    mock_class = mock.MagicMock()
    mock_class.once_called = []
    mock_class.method.return_value=True
    mock_class.method = annus.oncecalled(mock_class.method)
    assert mock_class.method(mock_class) == True
    assert mock_class.method(mock_class) == False

def test_contains(send_one_year_liturgical_calendar):
    L = send_one_year_liturgical_calendar
    assert datetime.date(1962,3,3) in L
    assert 1962 in L
    for i in range(1600,1962):
        assert i not in L
    for i in range(1963,4100):
        assert i not in L
        
def test_len(send_one_year_liturgical_calendar):
    L=send_one_year_liturgical_calendar
    assert len(L) == 1
    L(1975)
    assert len(L) == 2
    L(1975)
    assert len(L) == 2
    L(1990)
    assert len(L) == 3
    
def test_repr(send_empty_liturgical_calendar):
    assert send_empty_liturgical_calendar.__repr__(
        ) == """LiturgicalYear. {}/{}""".format(
            send_empty_liturgical_calendar.ordo,
            send_empty_liturgical_calendar.proper)
        
def test_str(send_empty_liturgical_calendar):
    L=send_empty_liturgical_calendar
    debut = random.randrange(1962,2000)
    fin = random.randrange(debut,2001)
    L(debut,fin)
    assert L.__str__() == """LiturgicalYear. Ordo : {}. Proper : {}. Years already loaded : {}.""".format(L.ordo,L.proper,", ".join(
        [str(year) for year in range(debut,fin+1)]))
        
@mock.patch("pickle.Unpickler")
@mock.patch("__main__.open")
def test_load_raw_data(mock_open,mock_unpickler):
    mock_load = mock.MagicMock()
    mock_load.load.return_value=[1,2]
    mock_unpickler.return_value = mock_load
    L = annus.LiturgicalCalendar()
    assert isinstance(getattr(L,'raw_data'),list)
    assert getattr(L,'saturday') == 1
    assert getattr(L,'feria') == 2
    for name, item in zip(annus.fichiers,mock_unpickler.call_args_list):
        assert name in item.__repr__() # pas terrible, mais on s'assure que l'appel a été fait à tous les fichiers. # TODO Tester l'existence des fichiers ?

def test_create_empty_year():
    year = random.randrange(1600,4100)
    empty_year = annus.LiturgicalCalendar.create_empty_year(year)
    date = datetime.date(year,1,1)
    while True:
        assert date in empty_year
        assert empty_year[date] == []
        date = date + datetime.timedelta(1)
        if date.year != year:
            break
        
def test_call():
    def _create_year(year):
        FakeCalendar.year_names.append(year)
        FakeCalendar.year_names.sort()
    FakeCalendar = mock.MagicMock()
    FakeCalendar.call = annus.LiturgicalCalendar.__call__
    FakeCalendar.year_names = []
    FakeCalendar._create_year = _create_year
    
    assert FakeCalendar.year_names == []
    FakeCalendar.call(FakeCalendar,1962)
    assert FakeCalendar.year_names == [1962]
    FakeCalendar.call(FakeCalendar,1962)
    assert FakeCalendar.year_names == [1962]
    FakeCalendar.call(FakeCalendar,1964,1966)
    assert FakeCalendar.year_names == [1962, 1964, 1965, 1966]
    assert FakeCalendar.call(FakeCalendar,1200) == False
    assert FakeCalendar.call(FakeCalendar,5000) == False
    assert FakeCalendar.call(FakeCalendar,1540,1700) == False
    assert FakeCalendar.call(FakeCalendar,3000,5000) == False
    assert FakeCalendar.call(FakeCalendar,2000,1995) == False
    assert FakeCalendar.year_names == [1962, 1964, 1965, 1966]
    
def test_iter(send_empty_liturgical_calendar):
    l=send_empty_liturgical_calendar
    l.year_names.append(2000)
    l.year_data[2000] = {}
    date = datetime.date(2000,1,1)
    date_list = []
    while True:
        date_list.append(date)
        item = FakeFeast(date=(date.month,date.day))
        item.DateCivile('easter',2000)
        l.year_data[2000][date] = [item]
        date = date + datetime.timedelta(1)
        if date.year != 2000:
            break
    for date, item in zip(date_list,l):
        assert date == item[0].date
    assert date.day, date.month == (31, 12)
    
def test_getitem(send_empty_liturgical_calendar):
    l=send_empty_liturgical_calendar
    l.raw_data=[item for item in FakeFeast_basic_iterator(1962) ]
    with pytest.raises(KeyError):
        l[1962]
    l(1962)
    assert 1961 in l.previous_year_names
    with pytest.raises(KeyError):
        l[1961]
        l[datetime.date(1961,1,1)]
    return l
    assert l[1962][datetime.date(1962,1,1)][0].date == datetime.date(1962,1,1)
    assert l[1962][datetime.date(1962,12,31)][0].date == datetime.date(1962,12,31)
    date = datetime.date(1962,4,5)
    extrait = l[date,datetime.date(1962,4,8)]
    for item in extrait :
        assert item[0].date == date
        date = date + datetime.timedelta(1)
    assert l[date,datetime.date(1962,1,1)] == []
    l(1963)
    date = datetime.date(1962,12,25)
    extrait = l[date,datetime.date(1963,1,8)]
    for item in extrait :
        assert item[0].date == date
        date = date + datetime.timedelta(1)
        
def test_setitem(send_empty_liturgical_calendar):
    l=send_empty_liturgical_calendar
    l.raw_data = [item for item in FakeFeast_basic_iterator(1962) ]
    l(1962)
    l[datetime.date(1962,1,1)] = 1
    assert l.year_data[1962][datetime.date(1962,1,1)] == 1
    l[datetime.date(1961,1,1)] = 1
    assert l.previous_year_data[1961][datetime.date(1961,1,1)] == 1
    with pytest.raises(KeyError):
        l.year_data[1961][datetime.date(1961,1,1)]
    l[datetime.date(1100,1,1)] = 1
    assert l.next_year_data[1100][datetime.date(1100,1,1)] == 1
    assert 1100 in l.next_year_names
    assert 1100 not in l.year_data
    assert 1100 not in l.previous_year_data
    
def test_put_in_year(send_empty_liturgical_calendar):
    l=send_empty_liturgical_calendar
    l._move = mock.MagicMock()
    args_tuple = (FakeFeast('Something'),FakeFeast('Otherone'),*FakeFeast_with_DateCivile_as_iterable().DateCivile(1,1))
    l.raw_data = [args_tuple[0],args_tuple[1], FakeFeast_with_DateCivile_as_iterable()]
    l._put_in_year(1962)
    assert l._move.call_count == 4
    for item in args_tuple:
        assert item.nom in str(l._move.call_args_list)
        
def test_create_year(send_empty_liturgical_calendar):
    l=send_empty_liturgical_calendar
    l._selection = mock.MagicMock()
    l._put_in_year = mock.MagicMock()
    l._create_year(1900)
    assert 1900 in l.year_names
    assert 1900 in l.year_data
    assert 1900 not in l.previous_year_names
    assert 1900 not in l.next_year_names
    l._put_in_year.assert_has_calls([mock.call(1900),mock.call(1899)])
    assert l._selection.call_count == 365 == len(l.year_data[1900])
    assert isinstance(l.year_data[1900][datetime.date(1900,1,1)],list)
    assert 1899 in l.previous_year_names
    l._create_year(1899)
    assert l.year_names == [1899,1900]
    assert 1899 not in l.previous_year_names
    l._create_year(1901)
    assert l.year_names == [1899,1900,1901]
    assert 1900 not in l.previous_year_names
    l.next_year_names.append(1902)
    l.next_year_data[1902] = {datetime.date(1902,1,1):[mock.MagicMock()]}
    l._create_year(1902)
    assert 1902 not in l.next_year_names
    assert 1902 not in l.next_year_data
    assert l.year_names == [1899,1900,1901,1902]
    assert 1901 not in l.previous_year_names
    l.next_year_names.append(1908)
    l.next_year_data[1908] = {datetime.date(1908,1,1):[mock.MagicMock()]}
    l._create_year(1909)
    assert 1908 not in l.next_year_names
    assert 1908 in l.previous_year_names
    
def test_move(send_empty_liturgical_calendar): # WARNING do not test local propers
    l=send_empty_liturgical_calendar
    l.year_names.append(1962)
    l.year_data[1962] = l.create_empty_year(1962)
    l.raw_data = (
        FakeFeast(nom='JustPutInList'),
        
        FakeFeast(nom='P&D=1',personne='john',priorite=234,date=(2,2)),
        FakeFeast(nom='P&D=2',personne='john',priorite=432,date=(2,2)),
        
        FakeFeast(nom='d=1,p=1700,D=3,3',degre=1,priorite=1700,date=(3,3)),
        FakeFeast(nom='d=1,p=1660,D=3,3 -> 3,6',degre=1,priorite=1660,date=(3,3)),
        FakeFeast(nom='d=1,p=1601,D=3,3 -> 3,7',degre=1,priorite=1601,date=(3,3)),
        FakeFeast(nom='d=2,p=900,D=3,5',degre=2,priorite=900,date=(3,5)),
        FakeFeast(nom='d=1,p=1650,D=3,4',degre=1,priorite=1650,date=(3,4)),
        
        FakeFeast(nom='d=2,p=900,D=3,8',degre=2,priorite=900,date=(3,8)),
        FakeFeast(nom='d=1,p=1650,D=3,8',degre=1,priorite=1650,date=(3,8)),
        
        FakeFeast(nom='d=1,p=1601,D=3,10 -> 3,11',degre=1,priorite=1601,date=(3,10)),
        FakeFeast(nom='d=1,p=1641,D=3,10',degre=1,priorite=1641,date=(3,10)),
        
        FakeFeast(nom='sunday,d=2,p=700,D=1,4',degre=2,priorite=700,date=(1,4),dimanche=True),
        FakeFeast(nom='d=1,p=1700,D=1,4',degre=1,priorite=1700,date=(1,4)),
        
        FakeFeast(nom='sunday,d=1,p=1700,D=1,7',degre=1,priorite=1700,date=(1,7),dimanche=True),
        FakeFeast(nom='d=1,p=1750,D=1,7',degre=1,priorite=1750,date=(1,7)),
        
        FakeFeast(nom='d=1,p=1601,D=12,31 -> 1,1',degre=1,priorite=1601,date=(12,31)),
        FakeFeast(nom='d=1,p=1641,D=12,31',degre=1,priorite=1641,date=(12,31)),
        )
    for item in l.raw_data:
        l._move(item,item.DateCivile(1,1962))
     
    YEAR = l.year_data[1962] 
    assert YEAR[datetime.date(1962,1,1)][0].nom == 'JustPutInList'
    assert YEAR[datetime.date(1962,1,4)][0].nom == 'd=1,p=1700,D=1,4'
    assert YEAR[datetime.date(1962,1,4)][1].nom == 'sunday,d=2,p=700,D=1,4'
    assert YEAR[datetime.date(1962,1,7)][0].nom == 'd=1,p=1750,D=1,7'
    assert YEAR[datetime.date(1962,1,7)][1].nom == 'sunday,d=1,p=1700,D=1,7' 
    assert YEAR[datetime.date(1962,2,2)][0].nom == 'P&D=2'
    assert YEAR[datetime.date(1962,2,2)][1].nom == 'P&D=1'
    assert YEAR[datetime.date(1962,3,3)][0].nom == 'd=1,p=1700,D=3,3'
    assert YEAR[datetime.date(1962,3,6)][0].nom == 'd=1,p=1660,D=3,3 -> 3,6'
    assert YEAR[datetime.date(1962,3,7)][0].nom == 'd=1,p=1601,D=3,3 -> 3,7'
    assert YEAR[datetime.date(1962,3,5)][0].nom == 'd=2,p=900,D=3,5'
    assert YEAR[datetime.date(1962,3,4)][0].nom == 'd=1,p=1650,D=3,4'
    assert YEAR[datetime.date(1962,3,8)][0].nom == 'd=1,p=1650,D=3,8'
    assert YEAR[datetime.date(1962,3,8)][1].nom == 'd=2,p=900,D=3,8'
    assert YEAR[datetime.date(1962,3,10)][0].nom == 'd=1,p=1641,D=3,10'
    assert YEAR[datetime.date(1962,3,11)][0].nom == 'd=1,p=1601,D=3,10 -> 3,11'
    assert YEAR[datetime.date(1962,12,31)][0].nom == 'd=1,p=1641,D=12,31'
    assert l.next_year_data[1963][datetime.date(1963,1,1)][0].nom == 'd=1,p=1601,D=12,31 -> 1,1'
    
    l.previous_year_names.append(1960)
    l.previous_year_data[1960] = l.create_empty_year(1960)
    for item in l.raw_data:
        l._move(item,item.DateCivile(1,1960))
        
    YEAR = l.previous_year_data[1960] 
    assert YEAR[datetime.date(1960,1,1)][0].nom == 'JustPutInList'
    assert YEAR[datetime.date(1960,1,4)][0].nom == 'd=1,p=1700,D=1,4'
    assert YEAR[datetime.date(1960,1,4)][1].nom == 'sunday,d=2,p=700,D=1,4'
    assert YEAR[datetime.date(1960,1,7)][0].nom == 'd=1,p=1750,D=1,7'
    assert YEAR[datetime.date(1960,1,7)][1].nom == 'sunday,d=1,p=1700,D=1,7' 
    assert YEAR[datetime.date(1960,2,2)][0].nom == 'P&D=2'
    assert YEAR[datetime.date(1960,2,2)][1].nom == 'P&D=1'
    assert YEAR[datetime.date(1960,3,3)][0].nom == 'd=1,p=1700,D=3,3'
    assert YEAR[datetime.date(1960,3,6)][0].nom == 'd=1,p=1660,D=3,3 -> 3,6'
    assert YEAR[datetime.date(1960,3,7)][0].nom == 'd=1,p=1601,D=3,3 -> 3,7'
    assert YEAR[datetime.date(1960,3,5)][0].nom == 'd=2,p=900,D=3,5'
    assert YEAR[datetime.date(1960,3,4)][0].nom == 'd=1,p=1650,D=3,4'
    assert YEAR[datetime.date(1960,3,8)][0].nom == 'd=1,p=1650,D=3,8'
    assert YEAR[datetime.date(1960,3,8)][1].nom == 'd=2,p=900,D=3,8'
    assert YEAR[datetime.date(1960,3,10)][0].nom == 'd=1,p=1641,D=3,10'
    assert YEAR[datetime.date(1960,3,11)][0].nom == 'd=1,p=1601,D=3,10 -> 3,11'
    assert YEAR[datetime.date(1960,12,31)][0].nom == 'd=1,p=1641,D=12,31'
    assert l.next_year_data[1961][datetime.date(1961,1,1)][0].nom == 'd=1,p=1601,D=12,31 -> 1,1'
    
