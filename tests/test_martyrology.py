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
    
@mock.patch('martyrology.Martyrology._get_data')
@mock.patch('martyrology.matcher.Matcher')    
def test_raw_kw(mock_matcher,get_data_method):
    matcher_instance = mock_matcher()
    matcher_instance.is_score_low.return_value = False
    matcher_instance.fuzzer.return_value = 1
    lines = ['a','ba','caa','daaa','bbaaa','ccaaaa',]
    get_data_method('lang').__getitem__.return_value = [[['a','ba','caa']],[['daaa','bbaaa','ccaaaa']],]
    tokens = ['token1','token2']
    lang = 'ja'
    m=martyrology.Martyrology()
    res = m._raw_kw(tokens,lang)
    mock_matcher.assert_called_with(tokens,lang)
    get_data_method.assert_called_with(lang)
    assert get_data_method().__getitem__.call_args_list == [mock.call('data')]
    assert matcher_instance.fuzzer.call_count == 6
    assert matcher_instance.fuzzer.call_args_list == [mock.call(elt) for elt in lines]
    assert matcher_instance.is_score_low.call_count == 1
    
    
    get_data_method('lang').__getitem__.return_value = [[['a','ba','caa']],[['daaa','bbaaa','ccaaaa']],[['c','b','j']],[['h','b','r','t']]]
    matcher_instance.fuzzer = lambda x : len(x)
    res = m._raw_kw(tokens,lang,max_nb_returned = 3)
    assert res[0].ratio == 6 and res[1].ratio == 3
    assert len(res) == 3
    
    res = m._raw_kw(tokens,lang,min_ratio = 3)
    assert len(res) == 2
    assert res[0].ratio >= res[1].ratio >= 3
    
    def is_score_low(x=[2]):
        x[0] -= 1
        return x[0]
    
    matcher_instance.is_score_low = is_score_low
    matcher_instance.fuzzer = mock.MagicMock()
    matcher_instance.fuzzer.return_value = 0.85
    res = m._raw_kw(tokens,lang)
    assert matcher_instance.splitter.call_count == 1
    assert matcher_instance.fuzzer.call_count == 13*2    
    
@mock.patch('martyrology.Martyrology.daytext')
@mock.patch('martyrology.Martyrology._raw_kw')
def test_kw(_raw_kw,daytext):
    item = mock.MagicMock()
    item.month = 1
    item.day = 10
    item.matching_line = 2
    _raw_kw.return_value = [item]
    m=martyrology.Martyrology()
    tokens = ['token1','token2']
    lang = 'ja'
    m.kw(tokens,lang,year=2000)
    _raw_kw.assert_called_once_with(tokens,lang,-1,.80)
    daytext.assert_called_once_with(datetime.date(2000,item.month,item.day),lang,item.matching_line)
