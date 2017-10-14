#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module defines a light json wrapper.
the class JWrapper allowed user to save & extract
custom classes in json"""

import importlib
import json
import phlog
import re

logger = phlog.loggers['console']

class JWrapper(json.JSONEncoder):
    """A global wrapper for special json objects"""
    def __init__(self,*p,**kw):
        json.JSONEncoder.__init__(self,*p,**kw) # a dict of types
        
        self.loaded_modules = {} # a dict of loaded modules
    
    def default(self,obj):
        """Main method. Called by json
        to serialise an object"""
        if isinstance(obj,re._pattern_type):
            returned_value = self._save_SRE_Pattern(obj)
        else:
            returned_value = self._custom_saver(obj)
        return returned_value
    
    def decode(self,obj):
        """Manage methods to decode obj"""
        if '__class__' in obj:
            if obj['__class__'] == re._pattern_type.__name__:
                obj = self._restore_SRE_Pattern(obj)
            else:
                obj = self._custom_restore(obj)
        return obj
    
    def save(self,obj,file_name,indent=0):
        """A simple wrapper of json.dump"""
        with open(file_name,'w') as file:
            json.dump(obj,file,cls=self.__class__,indent=indent)
    
    def restore(self,file_name):
        """A simple wrapper of json.load"""
        with open(file_name,'r') as file:
            return json.load(file,object_hook=self.decode)
            
    def _save_SRE_Pattern(self,obj):
        """Serialize SRE_Pattern"""
        return {'__class__':re._pattern_type.__name__,
                '__data__':obj.pattern}
    
    def _restore_SRE_Pattern(self,obj):
        """Return SRE_Pattern"""
        return obj['__data__']
        return re.compile(obj['__data__'])
    
    def _custom_saver(self,obj):
        """Serialize obj with dict to json format"""
        dico = obj.__dict__
        dico['__class__'] = type(obj).__name__
        dico['__module__'] = obj.__module__
        return dico
    
    def _custom_restore(self,obj):
        """Restore obj"""
        class_of_obj = self._load_class(obj['__class__'],obj['__module__'])
        del(obj['__class__'])
        del(obj['__module__'])
        future_obj = class_of_obj()
        future_obj.__dict__.update(obj)
        return future_obj
    
    def _load_module(self,module):
        """Load modules to load classes
        module : str"""
        if module not in self.loaded_modules:
            self.loaded_modules[module] = importlib.import_module(module)
        return self.loaded_modules[module]
    
    def _load_class(self,classe,module=None):
        """Load class"""
        module = self._load_module(module)
        return getattr(module,classe)
    
    
