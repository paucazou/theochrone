#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import dossier
dossier.main()
import gettext
import messages
import unittest.mock as mock
import pytest
from messages import MessagesTranslator

# test MessagesTranslator class

def test_init():
    """A useless test. But it will work. And it is good
    to see a test passed.
    Guess what? The first time it was called, it failed."""
    elt = MessagesTranslator('langs','lang')
    assert elt.langs == 'langs'
    assert elt.current_lang == 'lang'

@mock.patch('builtins._')
def test_getattr(underscore_mock):
    """test __getattr__ method"""
    underscore_mock.return_value = 'SOMETHING'
    elt = MessagesTranslator('langs','lang')
    elt.__dict__['_something'] = 'SOMETHING'
    assert elt.something == 'SOMETHING'
    assert underscore_mock.call_args == mock.call('SOMETHING') 
    with pytest.raises(AttributeError):
        elt.other

    assert elt.langs == 'langs'
    assert elt.current_lang == 'lang'

def test_setattr():
    """test __setattr__ method"""
    elt = MessagesTranslator('langs','lang')
    elt.something = 1
    with pytest.raises(AttributeError):
        elt._anything = 1
    with pytest.raises(AttributeError):
        elt.something = 2
    elt.god = 'GOD'
    assert '_god' in elt.__dict__
    assert 'god' not in elt.__dict__
    assert elt.__dict__['_god'] == 'GOD'
    assert '_current_lang' in elt.__dict__ and '_langs' in elt.__dict__
    elt.current_lang = 1
    elt.langs = 2
    assert elt.current_lang == 1
    assert elt.langs == 2

@mock.patch('messages.MessagesTranslator.__setattr__')
def test_markToTranslate(setattr_mock):
    elt = MessagesTranslator('langs','lang')
    return_value = elt.markToTranslate('SOME TEXT','NAME')
    setattr_mock.assert_called_with('NAME','SOME TEXT')
    assert return_value == 'SOME TEXT'

@mock.patch('builtins._')
@mock.patch('gettext.NullTranslations.install')
def test_get(install_mock,underscore_mock):
    """test get method"""
    underscore_mock.return_value='translation'
    langs = {
            'en':gettext.translation('messages',localedir='/',fallback=True),
            'fr':gettext.translation('messages',localedir='/',fallback=True)}
    elt = MessagesTranslator(langs, 'en')
    elt.__dict__['_trad'] = 'traduction'
    assert elt.get('trad','en') == 'translation'
    install_mock.assert_not_called()
    elt.get('trad','fr')
    install_mock.assert_called_once_with()
    assert elt.current_lang == 'fr'
    assert langs['fr'].install.call_count == 1
    elt.get('trad','es')
    assert elt.current_lang == 'en'
    assert langs['en'].install.call_count == 2
    with pytest.raises(AttributeError):
        elt.get('allah','en')

@mock.patch('gettext.NullTranslations.install')
def test_setLang(install_mock):
    """test setLang method"""
    langs = {
            'en':gettext.translation('messages',localedir='/',fallback=True),
            'fr':gettext.translation('messages',localedir='/',fallback=True)}
    elt = MessagesTranslator(langs, 'en')
    elt.setLang('en')
    install_mock.assert_not_called()
    elt.setLang('fr')
    assert langs['fr'].install.call_count == 1
    elt.setLang('fr')
    assert langs['fr'].install.call_count == 1
    elt.setLang('es')
    assert langs['en'].install.call_count == 2

