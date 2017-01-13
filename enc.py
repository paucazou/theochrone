#!/usr/bin/python3
#-*- coding: utf-8 -*-

#copyright 2016 clsergent
#prefs version 2.0.3
#licence GPLv3
#version de test

import io
import adjutoria
import datetime
from xml.etree.ElementTree import Element, ElementTree, XML

class Modele():
    """Une classe modèle pour les types non implémentés."""
    
    def __init__(self,classe='',att={}):
        self.classe=classe
        self.attributs=att

class PreferencesType:
    Element= Element
    """handle conversion from and to XML of the given type
    when created, the instance immediately add itself to Preferences types set
    PreferencesType.Element can be safely called for getObj and getXML implementation"""
    def __init__(self, *newtypes, tag= None, getobj= None, getxml= None):
        """create the new PreferencesType from the given newtype, and tag is used for XML labelling
        getobj and getxml are used for conversion from and to XML. If not provided, corresponding methods must be implemented"""
        self._types= newtypes
        if not tag:
            tag= newtypes[0].__name__
        self._tag= tag
        
        if callable(getobj):
            self.getObj= getobj
        if callable(getxml):
            self.getXML= getxml
        
        #directly added to Preferences types set
        #Preferences.addType(sef)
    
    def getObj(self, item, **kwds):
        """"return an instance of _type from an XML Element"""
        raise(NotImplementedError)
    
    def getXML(self, obj, **kwds):
        """return an XML Element from an instance of _type"""
        raise(NotImplementedError)
    
    def getTag(self):
        return self._tag
    
    def getTypes(self):
        return self._types
    
    tag= property(getTag, doc='tag used for XML formatting')
    types= property(getTypes, doc='types handled')

class PreferencesTypeModele(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, Modele)
        
    def getObj(self, item, **kwds):
        obj=Modele()
        for child in item.getchildren():
            obj.__dict__[child.get('key')]= Preferences.getObj(child)
        objetrenvoye=getattr(adjutoria,obj.classe)()
        objetrenvoye.__dict__=obj.attributs
        return objetrenvoye
    
    def getXML(self, obj, **kwds):
        item=Element(self.tag, **kwds)
        for key, value in obj.__dict__.items():
            item.append(Preferences.getXML(value, key=key))
        return item
   

class PreferencesTypeTimedelta(PreferencesType):
    
    def __init__(self):
        PreferencesType.__init__(self, datetime.timedelta)
        
    def getObj(self, item, **kwds):
        return datetime.timedelta(seconds=float(item.text))
    
    def getXML(self, obj, **kwds):
        item=Element(self.tag, **kwds)
        item.text=str(obj.total_seconds())
        return item
    

class PreferencesTypeString(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, str)
    
    def getObj(self, item, **kwds):
        return '' if item.text is None else item.text
        #return item.text
    
    def getXML(self, obj, **kwds):
        item= Element(self.tag, **kwds)
        item.text= obj
        return item

class PreferencesTypeInt(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, int)
    
    def getObj(self, item, **kwds):
        return int(item.text)
    
    def getXML(self, obj, **kwds):
        item= Element(self.tag, **kwds)
        item.text= str(obj)
        return item

class PreferencesTypeFloat(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, float)
    
    def getObj(self, item, **kwds):
        return float(item.text)
    
    def getXML(self, obj, **kwds):
        item= Element(self.tag, **kwds)
        item.text= str(obj)
        return item

class PreferencesTypeBool(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, bool)
    
    def getObj(self, item, **kwds):
        return eval(item.text)
    
    def getXML(self, obj, **kwds):
        item= Element(self.tag, **kwds)
        item.text= str(obj)
        return item
    
class PreferencesTypeNone(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, type(None), tag= 'None')
    
    def getObj(self, item, **kwds):
        return None
    
    def getXML(self, obj, **kwds):
        item= Element(self.tag, **kwds)
        return item

class PreferencesTypeDict(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, dict)
    
    def getObj(self, item, **kwds):
        obj= dict()
        for child in item.getchildren():
            try:
                if 'tH1s 1s AN InTEg3r' in child.get('key'):
                    key = child.get('key')[18:]
                    obj[int(key)] = Preferences.getObj(child)
                elif 'Th1s iS a FlOAt' in child.get('key'):
                    key = child.get('key')[15:]
                    obj[float(key)] = Preferences.getObj(child)
                elif 'tHIS 1 is a bo0l' in child.get('key'):
                    key = child.get('key')[16:]
                    if key == 'True':
                        obj[True] = Preferences.getObj(child)
                    else:
                        obj[False] = Preferences.getObj(child)
                else:
                    obj[child.get('key')]= Preferences.getObj(child)
            except ValueError:
                obj[child.get('key')]= Preferences.getObj(child)
        return obj
    
    def getXML(self, obj, **kwds):
        item= Element(self.tag, **kwds)
        for key, value in obj.items():
            if isinstance(key,bool):
                key = 'tHIS 1 is a bo0l' + str(key)
            elif isinstance(key,int):
                key = 'tH1s 1s AN InTEg3r' + str(key)
            elif isinstance(key,float):
                key = 'Th1s iS a FlOAt' + str(key)
            item.append(Preferences.getXML(value, key=key))
        return item
    
class PreferencesTypeList(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, list)
    
    def getObj(self, item, **kwds):
        obj= list()
        for child in item.getchildren():
            obj.append(Preferences.getObj(child))
        return obj
    
    def getXML(self, obj, **kwds):
        item= Element(self.tag, **kwds)
        for value in obj:
            item.append(Preferences.getXML(value))
        return item
    
class PreferencesTypeTuple(PreferencesType):
    def __init__(self):
        PreferencesType.__init__(self, tuple)
    
    def getObj(self, item, **kwds):
        obj= list()
        for child in item.getchildren():
            obj.append(Preferences.getObj(child))
        return tuple(obj)
    
    def getXML(self, obj, **kwds):
        item= Element(self.tag, **kwds)
        for value in obj:
            item.append(Preferences.getXML(value))
        return item
             
class Preferences(io.FileIO):
    types= {PreferencesTypeString(),
            PreferencesTypeInt(),
            PreferencesTypeFloat(),
            PreferencesTypeNone(),
            PreferencesTypeDict(),
            PreferencesTypeList(),
            PreferencesTypeTuple(),
            PreferencesTypeModele(),
            PreferencesTypeTimedelta(),
            PreferencesTypeBool(),
            }
    def __init__(self, *args, **kwds):
        io.FileIO.__init__(self, *args, **kwds)
    
    def _noIOAccess(func):
        def operation(*args, **kwds):
            raise(IOError, 'access to IO operations is not allowed')
        return operation
    
    @classmethod
    def addType(cls, newtype):
        """add a new PreferencesType to the types dictionnary"""
        if not isinstance(newtype, PreferencesType):
            cls._types.add(newtype)
    
    @classmethod
    def removeType(cls, oldtype):
        """remove a PreferencesType form the types dictionnary"""
        if oldtype in cls.types:
            cls.types.remove(oldtype)
    
    @classmethod
    def getType(cls, tag_or_type):
        """return the PreferencesType corresponding to tag_or_obj"""
        if isinstance(tag_or_type, str):
            for preftype in cls.types:
                if tag_or_type == preftype.tag:
                    return preftype
            return False
        else:
            for preftype in cls.types:
                if tag_or_type in preftype.types:
                    return preftype
            return False
    
    def get(self, noerror= False, **kwds):
        """get the content of the file parsed as XML"""
        if noerror:
            try:
                return cls.get(obj, noerror=False, **kwds)
            except:
                return False
        
        self.seek(0)
        raw= io.FileIO.read(self)
        return self.gets(raw, noerror)
        #except:
        return set()
    
    @classmethod
    def gets(cls, raw, noerror= False, **kwds):
        """return an object from an XML string"""
        if noerror:
            try:
                return cls.gets(obj, noerror=False, **kwds)
            except:
                return False
            
        item= XML(raw)
        return cls.getObj(item)
    
    def set(self, obj, noerror=False, **kwds):
        """write the obj as XML in the file"""
        if noerror:
            try:
                return cls.set(obj, noerror=False, **kwds)
            except:
                return False
        
        item= self.getXML(obj)
        self.truncate(0)
        self.seek(0)
        ElementTree(item).write(self, encoding= 'utf-8', xml_declaration=True)
        return True
    
    @classmethod
    def sets(cls, obj, noerror= False, **kwds):
        """return an XML string fro an object"""
        if noerror:
            try:
                return cls.sets(obj, noerror=False, **kwds)
            except:
                return False
            
        item= cls.getXML(obj)
        file= io.BytesIO()
        ElementTree(item).write(file, encoding= 'utf-8', xml_declaration=True)
        return file.getvalue()
    
    @classmethod
    def getObj(cls, item, **kwds):
        """"get obj from  an XML Element using types"""
        preftype= cls.getType(item.tag)
        if not preftype:
            raise NotImplementedError('support of {0} has not been implemented yet'.format(item.tag))
        else:
            return preftype.getObj(item, **kwds)
    
    @classmethod
    def getXML(cls, obj, **kwds):
        """get an XML Element from obj using types"""
        preftype= cls.getType(type(obj))
        if not preftype:
            try:
                obj=Modele(type(obj).__name__,obj.__dict__)
            except:
                raise NotImplementedError('support of {0} has not been implemented yet'.format(type(obj)))
            else:
                preftype=cls.getType(type(obj))
        return preftype.getXML(obj, **kwds)
    
    #legacy function, should not be used
    get_prefs= get
    set_prefs= set
    get_sprefs= gets
    set_sprefs= sets
    
    prefs= property(get, set, doc='access to the file')
        
def tostring(obj, noerror= False, **kwds):
    """convenient function to get an XML string from a given obj"""
    return Preferences.sets(obj, noerror, **kwds)

def fromstring(raw, noerror= False, **kwds):
    """convenient function to get an object from an XML string"""
    return Preferences.gets(raw, noerror, **kwds)
    
if __name__ == '__main__':
    print('this module is not intended to be used standalone')

