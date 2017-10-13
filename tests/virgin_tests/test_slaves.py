#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende



import os
import pytest
import sys
import unittest.mock as mock

os.chdir('..')
sys.path.append('.')
import dossier
dossier.main()
import virgin.slaves

class DBManager(mock.MagicMock):
    """Class that mocks virgin.virgindb.DBManager"""
    def __init__(self):
        mock.MagicMock.__init__(self)
        self.db_connected = True
        self.connect_call = 0
        self.close_call = 0
        self._restore_from_string_call = 0
        self._del_call = 0
    
    def connect(self):
        self.connect_call+=1
    
    def close(self):
        self.close_call+=1
    
    def _restore_from_string(self,something):
        self._restore_from_string_call+=1
    
    def __del__(self):
        self._del_call+=1

def test_StrLike():
    long_string = "l"*151
    long_string = virgin.slaves.StrLike(long_string)
    assert isinstance(long_string,virgin.slaves.LongStr)
    short_string = "l"*150
    short_string = virgin.slaves.StrLike(short_string)
    assert isinstance(short_string,virgin.slaves.ShortStr)
    with pytest.raises(AssertionError):
        virgin.slaves.StrLike(int())
        
def test_ShortStr():
    string = virgin.slaves.ShortStr("l"*150)
    assert isinstance(string,virgin.slaves.ShortStr)
    string = virgin.slaves.ShortStr("l"*151)
    assert isinstance(string,virgin.slaves.LongStr)
    assert issubclass(virgin.slaves.ShortStr,str) 
    
def test_LongStr():
    string = virgin.slaves.LongStr("l"*151)
    assert isinstance(string,virgin.slaves.LongStr)
    string = virgin.slaves.LongStr("l"*150)
    assert isinstance(string,virgin.slaves.ShortStr)
    assert issubclass(virgin.slaves.LongStr,str)
    
def test_Regex():
    regex_ = virgin.slaves._Regex("a regex")
    regex = virgin.slaves.Regex("another regex")
    assert issubclass(virgin.slaves._Regex,str)
    assert issubclass(virgin.slaves.Regex,str)
    
def test_BaseDict():
    dico = {1:1,2:2}
    obj = virgin.slaves.BaseDict("name",dico)
    assert obj.name == "name"
    assert obj == dico
    obj = virgin.slaves.BaseDict("name",a=2,b=1)
    assert obj == {'a':2,'b':1}
    obj = virgin.slaves.BaseDict("name",[(1,1),(2,2)])
    assert obj == {1:1,2:2}
    obj = virgin.slaves.BaseDict("namz",[(1,1),(2,2)],a=2,b=1)
    assert obj == {1:1,2:2,'a':2,'b':1}
    
Lazy = virgin.slaves.Lazy
def test_Lazy_with_no_arg():
    with pytest.raises(ValueError):
        obj = Lazy()

def test_Lazy_with_value_arg():
    base_obj = [1,2,3]
    obj = Lazy(value=base_obj)
    obj.db = mock.MagicMock()
    assert obj() == base_obj
    assert obj.value == obj._value == base_obj
    obj.db.connect.assert_not_called()
    obj.db._restore_from_string.assert_not_called()
    obj.value = 1
    assert obj.value == obj._value == 1
    obj.__call__ = mock.MagicMock()
    assert not obj.__call__.called
    obj.value
    assert obj.__call__.called
    
def test_Lazy_repr():
    pass

def test_Lazy_with_db_arg():
    pass
    

