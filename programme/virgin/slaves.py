#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module defines some classes used by virgindb"""
from re import match
# Classes
    
class StrLike: # pretty useless, no ? # TEST
    """This class is used to select which subclass
    of str fit to the value"""
    def __new__(cls,value):
        assert isinstance(value,str)
        return [ShortStr,LongStr][len(value) > 150](value)
    
class ShortStr(str): # TEST
    """A string whith len <= 150"""
    def __init__(self,value):
        if len(value) > 150:
            self.__class__ = LongStr
            self.__init__(value)
        str.__init__(self)
        
class LongStr(str):# TEST
    """A string whith len > 150"""
    def __init__(self,value):
        if len(value) <= 150:
            self.__class__ = ShortStr
            self.__init__(value)
        str.__init__(self)
        
class _Regex(str):# TEST
    """A class of strings used for regex"""
    def __init__(self,value):
        str.__init__(self)
        
class Regex(str): # TEST
    """A class of regex"""
    def __init__(self,value):
        str.__init__(self)
        
class BaseDict(dict): # TEST
    """A class to save a dict as a table"""
    def __init__(self,name,map_or_seq=None,**values):
        """values is a sequence as used in dict"""
        self.name = name
        if map_or_seq:
            values.update(dict(map_or_seq))
        dict.__init__(self,values)
        
class Lazy:
    """A Lazy object waits until it is called"""
    
    def __init__(self,db=None,raw_data=None,type_of_data=None,value=None):
        """Inits Lazy object.
        Warning : type of db and
        syntax of raw_data are not fully verified"""
        if not db and not value:
            raise ValueError("A Lazy object must have either a value or a DBManager")
        if raw_data and not match(".+/[.\w]+@\w+$",raw_data):
            raise SyntaxError("raw_data has incorrect syntax : " + raw_data)
        if db and db.__class__.__name__ != "DBManager":
            raise TypeError("db doesn't seem to be a DBManager object")
        self.db = db # db must be a DBManager object
        self.raw_data = raw_data # raw_data must have following structure : data/module@type
        self._value = value
        
    def __call__(self):
        """Returns object. Loads it if not already loaded"""
        if not self._value:
            db_was_closed = False
            if not self.db.db_connected:
                db_was_closed = True
                self.db.connect()
            self._value = self.db._restore_from_string(self.raw_data)
            if db_was_closed:
                self.db.close()
            del(self.db)
        return self._value
    
    def __repr__(self):
        """A Lazy object is waiting
        if self._value is not accessible
        Loaded after"""
        is_waiting = not self._value
        return "{} : {}".format(
            ("Loaded","Waiting")[is_waiting],
            (self._value,self.raw_data)[is_waiting])
            
    @property
    def value(self): #TEST
        """Alias of __call__"""
        return self.__call__()
    
    @value.setter 
    def value(self,value): #TEST
        """Set self._value"""
        self._value = value
        
