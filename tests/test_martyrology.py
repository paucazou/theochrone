#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import datetime
import dossier
import os
import pytest
import random
import subprocess
import unittest.mock as mock

dossier.main()
import martyrology

@mock.patch('os.listdir')
def test_init(listdir):
    listdir.return_value = ["fr_roman_martyrology_{}.pkl".format(year) for year in range(1950,1970)] + ["en_roman_martyrology_{}.pkl".format(year) for year in range(1950,1970)] + ["la_roman_martyrology_{}.pkl".format(year) for year in range(1950,1970)]
    file_path = martyrology.file_path
    m = martyrology.Martyrology()
    assert m._data == {lang:file_path + 'data/' + '{}_roman_martyrology_1962.pkl'.format(lang) for lang in ('fr','en','la')}
    m = martyrology.Martyrology(1965)
    assert m._data == {lang:file_path + 'data/' + '{}_roman_martyrology_1965.pkl'.format(lang) for lang in ('fr','en','la')}
    
@mock.patch('martyrology.humandate.main')
@mock.patch('martyrology.humandate.months')
@mock.patch('martyrology.Martyrology._get_data')
def test_daytext(get_data_method,hmonths,hmain):
    m=martyrology.Martyrology()
    for lang in ('fr','la'):
        result = m.daytext(datetime.date.today(),lang)
        assert isinstance(result,martyrology.TextResult)
        assert mock.call(lang) in get_data_method.call_args_list
        assert result.last_sentence == martyrology.Martyrology._last_line[lang]
        assert result.matching_line is None
    assert get_data_method.call_count == 2
    assert hmain.call_count == 2
    assert hmonths.__getitem__.call_count == 2
    result = m.daytext(datetime.date.today(),lang,2)
    assert result.matching_line == 2
    
    # 2 or 3 of November
    result = m.daytext(datetime.date(2014,11,3),'fr')
    get_data_method().__getitem__.assert_called_with('faithful_departed')
    result = m.daytext(datetime.date(2017,11,2), 'fr')
    get_data_method().__getitem__.assert_called_with('faithful_departed')
    
    # leap year
    for day in range(25,30):
        result = m.daytext(datetime.date(2000,2,day),'la')
        get_data_method().__getitem__('data').__getitem__(1).__getitem__.assert_called_with(day-2)
    for day in range(25,29):
        
        result = m.daytext(datetime.date(2001,2,day),'la')
        get_data_method().__getitem__('data').__getitem__(1).__getitem__.assert_called_with(day-1)
        
@mock.patch('martyrology.pickle')
def test_get_data(patch_pickle):
    m=martyrology.Martyrology()
    lang = 'fr'
    m._get_data(lang)
    patch_pickle.Unpickler.assert_any_call
    assert patch_pickle.Unpickler.call_count == 1
    m._get_data(lang)
    assert patch_pickle.Unpickler.call_count == 1

@mock.patch('martyrology.Martyrology._get_data')
def test_credits(get_data_method):
    m=martyrology.Martyrology()
    lang = 'ja'
    m.credits(lang)
    assert mock.call(lang) in get_data_method.call_args_list
    assert mock.call('credits') in get_data_method().__getitem__.call_args_list
    
