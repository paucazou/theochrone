#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import datetime
import json
import os
import pytest
import sys
import dossier
import unittest.mock as mock
from test_annus import FakeFeast
dossier.main()

import adjutoria
adjutoria.images = None

def fete_base():
    fete1 = adjutoria.Fete()
    fete1.degre = 1
    fete1._priorite = 1800
    fete1._temps_liturgique = 'Sometimes'
    return fete1

# Test Fete
def test_lt():
    fete1 = fete_base()
    autrefete = adjutoria.Fete()
    autrefete.degre = 3
    autrefete._priorite = 550
    assert fete1.__lt__(autrefete)
    autrefete.degre = 1
    assert fete1.__lt__(autrefete)
    
def test_hash():
    fete = adjutoria.Fete()
    hache = hash(fete)
    attr_dict = fete.__dict__.copy()
    assert not (attr_dict is fete.__dict__)
    del(attr_dict['parent'])
    attr_dict['personne'] = str(attr_dict['personne'])
    assert hash(fete) == hache == hash(json.dumps(attr_dict,sort_keys=True))
    fete.parent = 1
    assert hash(fete) == hache == hash(json.dumps(attr_dict,sort_keys=True))
    
def test_eq():
    fete1 = fete_base()
    fete2 = fete_base()
    with pytest.raises(TypeError):
        fete1.__eq__(1)
    assert fete1.__eq__(fete2)
    fete2.valeur = 4
    assert not fete2.__eq__(fete1)

def test_copy():
    fete1 = fete_base()
    fete2 = fete1.copy()
    assert fete1 == fete2 and not(fete1 is fete2)

@mock.patch('adjutoria.Fete.DateCivile_')    
def test_DateCivile(DateCivile_):
    fete = fete_base()
    fete.DateCivile(datetime.date.today(),1962)
    fete.date = datetime.date.today()
    assert DateCivile_.call_count == 1
    assert mock.call(datetime.date.today(),1962) in DateCivile_.call_args_list
    
def test_weeknumber():
    fete = adjutoria.Fete()
    fete.date = datetime.date(2015,1,1)
    assert fete.weeknumber() == 1 and fete.weeknumber(month=False,year=True) == 1
    assert fete.weeknumber(month=False,year=False) == fete.weeknumber(month=True,year=True) == (1,1)
    fete.date = datetime.date(2016,1,1)
    assert fete.weeknumber() == 1 and fete.weeknumber(month=False,year=True) == 0
    assert fete.weeknumber(month=False,year=False) == fete.weeknumber(month=True,year=True) == (1,0)
    fete.date = datetime.date(2000,12,31)
    assert fete.weeknumber(month=False,year=True) == 53
    for day in (10,11,12,13,14,15,16):
        fete.date = datetime.date(2016,1,day)
        assert fete.weeknumber() == 3
    fete.date = datetime.date(2017,1,1)
    assert fete.weeknumber(year=True) == (1,1)
    fete.date = datetime.date(2022,1,1)
    assert fete.weeknumber(year=True) == (1,0)
    
    
def test_paques():
    fete = fete_base()
    fete.date = datetime.date(1962,4,21)
    easter = datetime.date(1962,4,22)
    assert fete.DatePaques(easter,1962) == datetime.timedelta(1)
    
def test_temps_liturgique():
    fete = fete_base()
    assert fete.temps_liturgique() == 'Sometimes'
    fete._temps_liturgique = 'variable'
    fete.date = datetime.date(1962,1,1)
    fete.parent = mock.MagicMock()
    fete2 = adjutoria.Fete()
    fete2.temporal = True
    fete2._temps_liturgique = 'A time'
    fete.parent.__getitem__.return_value = [fete2]
    assert fete.temps_liturgique() == fete2._temps_liturgique
    assert mock.call(fete.date) in fete.parent.__getitem__.call_args_list
    assert fete.parent.__getitem__.call_count == 1

def test_set_transferee():
    fete = fete_base()
    fete.date = datetime.date(1962,1,1)
    assert not fete.transferee and not fete.date_originelle
    fete.transferee = True
    assert fete.transferee and fete.date_originelle == datetime.date(1962,1,1) and fete.date == datetime.date(1962,1,2)
    fete.transferee = True
    assert fete.transferee and fete.date_originelle == datetime.date(1962,1,1) and fete.date == datetime.date(1962,1,3)

@mock.patch('adjutoria.images')    
def test_get_images(images):
    images.get.return_value = None
    fete = fete_base()
    assert fete._images is '' and fete.images == fete._get_images() == None
    fete._images = "Fete"
    assert fete._images == "Fete" and fete.images == fete._get_images() == None
    images.get.return_value = True
    images.__getitem__.return_value = "Yes"
    assert fete.images == fete._get_images() == "Yes"
    assert images.__getitem__.call_count == 2 and mock.call(fete._images) in images.__getitem__.call_args_list
    
# test FeteFixe
def test_DateCivile_FeteFixe():
    fete = adjutoria.FeteFixe()
    fete.date_['mois'] = 1
    fete.date_['jour'] = 1
    assert fete.DateCivile_(None,1962) == datetime.date(1962,1,1)
    
# test FeteFixeBissextile

def test_DateCivile_FeteFixeBissextile():
    fete = adjutoria.FeteFixeBissextile()
    fete.date_['bissextile']['mois'] = 2
    fete.date_['bissextile']['jour'] = 29
    fete.date_['ordinaire']['mois'] = 2
    fete.date_['ordinaire']['jour'] = 28
    assert fete.DateCivile_(None,2000) == datetime.date(2000,2,29)
    assert fete.DateCivile_(None,2001) == datetime.date(2001,2,28)
    
#test FeteMobilePaques

def test_DateCivile_FeteMobilePaques():
    fete = adjutoria.FeteMobilePaques()
    fete.date_ = -2
    assert fete.DateCivile_(datetime.date(1962,4,22),1962) == datetime.date(1962,4,20)
    
# test FeteMobileDerniersDimanchesPentecote

def test_DateCivile_FeteMobileDerniersDimanchesPentecote():
    fete = adjutoria.FeteMobileDerniersDimanchesPentecote()
    fete.date_[238] = 2
    assert fete.DateCivile_(datetime.date(1943,4,25), 1943) == datetime.date(1943,4,27)
    assert fete.DateCivile_(datetime.date(2010,4,4), 2010) == datetime.date(2010,11,21)
    assert fete.priorite == 0
    
# test FeteMobileAvent

def test_DateCivile_FeteMobileAvent():
    fete = adjutoria.FeteMobileAvent()
    fete.date_ = 3
    assert fete.DateCivile_(None,2001) == datetime.date(2001,12,20)
    assert ('tuesday','jeudi','de Feria quinta') == (fete.nom_passager['en'], fete.nom_passager['fr'], fete.nom_passager['la'])
    fete2 = adjutoria.FeteMobileAvent()
    fete.date_ = -1
    assert fete.DateCivile_(None,2000) == datetime.date(2000,12,24) and fete._priorite == 0 and fete.commemoraison_privilegiee == -1
    
# test FeteMobileEpiphanie

def test_DateCivile_FeteMobileEpiphanie():
    fete = adjutoria.FeteMobileEpiphanie()
    fete.date_ = 2
    assert fete.DateCivile_(datetime.date(1900,4,15),1900) == datetime.date(1900,1,9)
    fete.date_ = 40
    assert fete.DateCivile_(datetime.date(1900,4,15),1900) == datetime.date(1900,2,11) == datetime.date(1900,4,15) - datetime.timedelta(63)
    assert fete._priorite == 0 and fete.commemoraison_privilegiee == -1
    
def test_get_couleur_FeteMobileEpiphanie():
    fete = adjutoria.FeteMobileEpiphanie()
    fete._couleur = 'rose bonbon'
    fete.date = datetime.date(2222,1,13)
    assert fete._couleur == fete.couleur == 'rose bonbon'
    fete.date = datetime.date(2222,1,15)
    assert fete._couleur == 'rose bonbon' and fete.couleur == 'vert'
    
# test FeteMobileMois
def test_DateCivile_FeteMobileMois():
     fete = adjutoria.FeteMobileMois()
     fete.date_['mois'], fete.date_['jour'], fete.date_['ordre'] = 10, 1, 0
     assert fete.DateCivile_(None,2000) == datetime.date(2000,10,3)
     fete.date_['mois'], fete.date_['jour'], fete.date_['ordre'] = 10, 6, 0
     assert fete.DateCivile_(None,2000) == datetime.date(2000,10,1)
     fete.date_['mois'], fete.date_['jour'], fete.date_['ordre'] = 10, 2, -1
     assert fete.DateCivile_(None,2000) == datetime.date(2000,10,25)
     fete.date_['mois'], fete.date_['jour'], fete.date_['ordre'] = 10, 0, -1
     assert fete.DateCivile_(None,2000) == datetime.date(2000,10,30)
     
     
# test FeteFixeTransferableDimanche
def test_DateCivile_FeteFixeTransferableDimanche():
    fete = adjutoria.FeteFixeTransferableDimanche()
    fete.date_['mois'], fete.date_['jour'] = 1,1
    fete.ecart_dimanche = 0
    fete.apres = True
    assert fete.DateCivile_(None,1789) == datetime.date(1789,1,4)
    fete.apres = False
    assert fete.DateCivile_(None,1789) == datetime.date(1788,12,28)
    fete.ecart_dimanche = 3
    assert fete.DateCivile_(None,1789) == datetime.date(1788,12,7)
    
# test FeteMobileCivile
def test_FeteMobileCivile():
    fete = adjutoria.FeteMobileCivile()
    fete.jour_de_semaine = 3
    fete.date_['mois'], fete.date_['jour'] = 1,1
    assert fete.DateCivile_(None,1789) == datetime.date(1788,12,31)
    fete.jour_de_semaine = 4
    assert fete.DateCivile_(None,1789) == datetime.date(1789,1,1)
    
# test FeteFerie

@mock.patch('officia.affiche_temps_liturgique')
@mock.patch('officia.nom_jour')
def test_QuelNom(Ltime_patch,Nday_patch):
    Ltime_patch.return_value = 'feria'
    Nday_patch.return_value = 'Liturgical time'
    fete = adjutoria.FeteFerie()
    return_value = fete.QuelNom(datetime.date(2017,6,20))
    assert return_value['la'] == 'Feria'
    assert return_value['en'] == 'Feria'
    assert return_value['fr'] == 'Feria de la férie du Liturgical time'

@mock.patch('adjutoria.FeteFerie.QuelNom')
def test_CreateFeria(name):
    fetes = adjutoria.FeteFerie()
    lcalendar = mock.MagicMock()
    first = FakeFeast(dimanche=True)
    first.link = '1link'
    first.addendum = "1addendum"
    first.propre = "1propre"
    first.couleur = "1color"
    first._temps_liturgique = '1ltime'
    zero = FakeFeast()
    zero.repris_en_ferie = False
    lcalendar.unsafe_iter.return_value = (
        False,[zero,first])
    return_value = fetes.CreateFeria(datetime.date(2000,1,1),lcalendar)
    assert (return_value.link, return_value.addendum, return_value.propre, return_value.couleur, return_value._temps_liturgique
            ) == (first.link, first.addendum, first.propre, first.couleur, first._temps_liturgique)
    assert isinstance(return_value,adjutoria.FeteFerie) and return_value.date == datetime.date(2000,1,1)
    assert return_value.parent is lcalendar
    name.assert_called_with(datetime.date(2000,1,1))
    assert mock.call(stop=datetime.date(2000,1,1),reverse=True) == lcalendar.unsafe_iter.call_args_list[-1]
    first.temps_liturgique = 'epiphanie'
    return_value = fetes.CreateFeria(datetime.date(2000,1,15),lcalendar)
    assert return_value.couleur == 'vert' and return_value._temps_liturgique == 'apres_epiphanie'

# test Samedi
def test_Samedi_Est_ce_samedi():
    fete = adjutoria.Samedi()
    assert fete.Est_ce_samedi(datetime.date(1715,1,12)) and fete.date == datetime.date(1715,1, 12)
    for day in 7, 8, 9, 10, 11, 13:
        assert not fete.Est_ce_samedi(datetime.date(1715,1,day))
        
# test TSNJ
@mock.patch('calendar.monthcalendar')
def test_DateCivile_TSNJ(month_patch):
    fete = adjutoria.TSNJ()
    fete.date_['mois'], fete.date_['jour'] = 1, 2
    for i in range(2,6):
        month_patch().__getitem__().__getitem__.return_value = i
        assert fete.DateCivile_(None,2000) == datetime.date(2000,1,i) and fete.dimanche
    for i in (1,6,7,8):
        month_patch().__getitem__().__getitem__.return_value = i
        assert fete.DateCivile_(None,2000) == datetime.date(2000,1,2) and not fete.dimanche
        
# test Defunts
def test_get_priorite_Defunts():
    fete = adjutoria.Defunts()
    for i in range(1,8):
        fete.date = datetime.date(2000,1,i)
        if datetime.date.isoweekday(fete.date) == 7:
            assert fete._get_priorite() == 1499
        else:
            assert fete._get_priorite() == 2100
    
# test DimancheOctaveNoel
@mock.patch('officia.dimancheapres')
def test_DateCivile_DimancheOctaveNoel(dimancheapres):
    fete = adjutoria.DimancheOctaveNoel()
    dimancheapres.return_value = datetime.date(2000,1,1)
    fete._priorite = 42
    assert fete.DateCivile_(None,1999) == dimancheapres() and fete._priorite == 0
    dimancheapres.return_value = datetime.date(1999,12,30)
    fete._priorite = 42
    assert fete.DateCivile_(None,1999) == dimancheapres() and fete._priorite == 42
    
# test JoursOctaveDeNoel
@mock.patch('officia.renvoie_regex')
def test_DateCivile_JoursOctaveDeNoel(renvoi):
    fetes = adjutoria.JoursOctaveDeNoel()
    renvoi.return_value = [None]
    j = 0
    for fete,i in zip(fetes.DateCivile(None,1701),fetes.date_):
        assert isinstance(fete,adjutoria.FeteFixe)
        assert not(fete.__dict__ is fetes.__dict__)
        assert fete.regex == [None]
        assert fete.date == datetime.date(1701,12,i)
        for langue in ('fr','la','en'):
            assert fete.nom[langue] == fetes.complements_nom[langue][j] + ' ' + fetes.nom_[langue]
        j += 1
    assert renvoi.call_count == j
    
# test JoursAvent
@mock.patch('officia.renvoie_regex')
def test_DateCivile_JoursAvent(renvoi):
    fetes = adjutoria.JoursAvent()
    renvoi.return_value = [None]
    for fete, i in zip(fetes.DateCivile(None,1701), fetes.date_):
        assert isinstance(fete,adjutoria.FeteMobileAvent)
        assert fete.date == fete.DateCivile_(None,1701)
        assert not(fete.__dict__ is fetes.__dict__)
        assert fete.regex == [None]
        for langue in ('fr','la','en'):
            if i > 14:
                assert fetes.nom_[langue][0] in fete.nom[langue]
                semaine = 1
            elif 6 < i < 15:
                assert fetes.nom_[langue][1] in fete.nom[langue]
                semaine = 2
            elif 0 < i < 7:
                assert fetes.nom_[langue][2] in fete.nom[langue]
                semaine = 3
            else:
                assert fetes.nom_[langue][3] in fete.nom[langue]
                semaine = 4
            if langue == 'fr':
                    assert mock.call(fete,None,[fete.nom_passager[langue],semaine]) == renvoi.call_args_list[-1]
        if fete.date.day > 16:
                assert fete.degre == 2
                assert fete._priorite == 1200
    
