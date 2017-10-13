#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module defines a class DBManager.
It's a wrapper of a sqlite3 database.
It can save following datatypes : 
int,float,str,NoneType,bytes,
list, tuple, dict, bool.
Custom classes with a __dict__ attribute can also be saved.
You can also save your own specific types by creating 
custom adapter & converter and register them
in DBManager.builtin : YourType:(self.adapters.adapt_YourType,self.adapters.convert_YourType)
str are saved in a very specific manner :
str longer than 150 characters are saved in a LongStr table,
whereas lower than 151 characters are saved in a ShortStr table.
dict can be saved as a string (like list)
or as a specific table, with the BaseDict class.
It can be useful if you have many dicts with exactly the same keys.
"""

import builtins
import collections
import importlib
import os
import phlog
import sqlite3
import virgin.adapters as adapters
import virgin.slaves as slaves

logger = phlog.loggers['console']
type_of = adapters.type_of
long_or_short = adapters.long_or_short
builtins.NoneType = type(None)
base_types = (int,float,bytes,builtins.NoneType)

# class

class DBManager():
    """Manages the database"""
    
    def __init__(self,base):
        """base is a pathlike object"""
        self.adapters = adapters.Adapter(self)
        
        if not os.path.isfile(base):
            already_exists = False
        else:
            already_exists = True
        self._base_path = base
        self.connect()
        if not already_exists:
            self._create_main()
        self.loaded_modules = {}
        
        self.builtin = { # changer cela : un tuple (adapter,converter)
            list: (self.adapters.adapt_list,self.adapters.convert_list),
            tuple:(self.adapters.adapt_list,self.adapters.convert_tuple),
            dict:(self.adapters.adapt_dict,self.adapters.convert_dict),
            bool:(self.adapters.adapt_bool,self.adapters.convert_bool),
            int:(self.adapters.adapt_int,self.adapters.convert_int),
            str:(self.adapters.adapt_str,self.adapters.convert_str),
            builtins.NoneType:(self.adapters.adapt_None,self.adapters.convert_None),
            slaves.BaseDict:(self.adapters.adapt_BaseDict,self.adapters.convert_BaseDict),
            slaves.Lazy:(self.adapters.adapt_Lazy,self.adapters.convert_Lazy),
            }
        for class_name in adapters.str_like_classes:
            class_ = getattr(slaves,class_name)
            adapter = self.adapters.adapt_str
            converter = getattr(self.adapters,'convert_'+class_name)
            self.builtin[class_] = (adapter,converter)
        
            
        custypes = self.fetchall("""SELECT name,module FROM custypes""")
        logger.debug(custypes)
        # registering custom converters
        for type_name, type_module in custypes:
            sqlite3.register_converter(type_name,self.custom_restore)
        self.custypes = {custype:(self.custom_saver,self.custom_restore) for custype in custypes}
        self.alltypes = collections.ChainMap(self.builtin,self.custypes)
        
    def __del__(self):
        logger.info("DBManager is about to be deleted")
        self.db.close()
    
    def close(self):
        """close base"""
        logger.info("Base is now closed")
        self.db.close()
        self.db_connected = False
        
    def connect(self):
        """Connect database."""
        logger.info("Base is now connected")
        self.db = sqlite3.connect(self._base_path)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.db_connected = True
        
    def _create_main(self): # TODO faire une table pour les images ?
        """Creates a virgin base with a main table.
        main table consists in an ID, a name and and a type columns.
        The ID of the main object is the same in the whole database.
        The custypes is the table of custom types to which refers the type column of the main table"""
        self.execute("""CREATE TABLE custypes(
            id INTEGER PRIMARY KEY,
            name TEXT,
            module TEXT);""")
        self.execute("""CREATE TABLE ShortStr( 
            id INTEGER PRIMARY KEY,
            text TEXT);""") # for strings <= 150
        self.execute("""CREATE TABLE LongStr(
            id INTEGER PRIMARY KEY,
            text TEXT);""") # for strings > 150
        self.execute("""CREATE TABLE _Regex(
            id INTEGER PRIMARY KEY,
            text TEXT);""") # for strings used for regex
        self.execute("""CREATE TABLE Regex(
            id INTEGER PRIMARY KEY,
            text TEXT);""") # for regex
        
    def create_table(self, table_name, **elts):
        """Create a new table.
        table_name : string
        elts : names parameters with following syntax : name = type
        do not include id in elts : it is already created by this method
        example : self.create_table('customers',name=str,age=int,basket=list)"""
        values = ','.join(["{} {}".format(name,self.storing_type(qtype)) for name, qtype in elts.items() ])
        command = """CREATE TABLE {} (
        id INTEGER PRIMARY KEY,
        {});""".format(table_name,values)
        for qtype in elts.values():
            self.update_custypes(qtype)
        self.execute(command)
        
    def save_row(self, table_name,id=0,*data): # TODO update data
        """Save a row into a table.
        If row (ie, id) already exist, update it
        else insert data with last id
        table_name : string
        id : int
        data : objects without id ; must be in the right order        
        return id"""
        laine = len(data) # laine in french has similar pronunciation to len in globish : funny, isn't it ?
        if not id:
            id = self.get_new_id(table_name)
            for i, elt in enumerate(data):
                if type(elt) not in base_types:
                    data[i] = "{}/{}".format(self._saver(elt),self._type_manager(type_entered=type_of(elt)))
            data.insert(0,id)
            command = """INSERT INTO {} values ({}?);""".format(table_name,"?, " * laine)
        self.execute(command,data)
        return id
        
    def restore_row(self,table_name,returned_type=dict,**where): # TODO faire une fonction similaire où il faudrait rentrer la ligne sql, dont le where serait modifié
        """restore data from table_name.
        where are named parameters where key is a column name
        and value is value requested. if where is empty, all values are returned
        returned_type is the type of the objects returned inside list returned.
        types available : dict (default), list, tuple"""
        # comment vérifier que ce qui a été rentré : on fait renvoyer None si on ne trouve pas ? Il faut un simulateur
        command = """SELECT * FROM {}""".format(table_name)
        if returned_type not in (dict,list,tuple):
            raise TypeError("returned_type must be a dict, a list or a tuple")
        logger.debug(where)
        if where:
            laine = len(where) - 1
            command += ' WHERE {} = {}' + " AND {} = {}" *laine
            list_of_replace = []
            for key, value in where.items():
                if type(value) not in base_types:
                    pass # TODO simulateur
                list_of_replace += [key,value]
            command = command.format(*list_of_replace)
        command += ';'
        raw_data = self.fetchall(command)
        returned_list = []
        logger.debug(returned_type)
        for row_object in raw_data:
            if returned_type is dict:
                tmp_container = {}
                for key,value in dict(row_object).items():
                    value = self._restore_from_string(value)
                    tmp_container[key] = value
            
            elif returned_type is not dict:
                tmp_container = [self._restore_from_string(value) for value in row_object]
                tmp_container = returned_type(tmp_container)                
            returned_list.append(tmp_container)
        return returned_list       
        
    def execute(self,*command):
        """Executes the command (any SQL command)
        Commits just after"""
        logger.debug(command)
        self.cursor.execute(*command)
        self.db.commit()
        
    def fetchone(self,*command):
        """Similar to execute, but return
        the result of self.cursor.fetchone()"""
        logger.debug(command)
        self.cursor.execute(*command)
        return self.cursor.fetchone()
    
    def fetchall(self,*command):
        """Similar to fetchone, but return
        the result fo self.cursor.fetchall()"""
        logger.debug(command)
        self.cursor.execute(*command)
        return self.cursor.fetchall()
        
    def get_last_id(self,table_name):
        """A method to get the last ID of a table"""
        self.cursor.execute("SELECT max(id) FROM {}".format(table_name))
        return self.cursor.fetchone()[0]
    
    def get_new_id(self,table_name):
        """A method to get the last id + 1"""
        last_id = self.get_last_id(table_name)
        return last_id + 1 if last_id else 1
    
    
    def _saver(self,queuer):
        """Save queuer in base.
        Return id if queur is saved as an int,
        else the string representing that data"""
        qtype = type_of(queuer)
        logger.debug(qtype)
        
        if (qtype.__name__,qtype.__module__) in self.alltypes:
            del(self.alltypes[(qtype.__name__,qtype.__module__)])
            del(self.custypes[(qtype.__name__,qtype.__module__)])
            self.custypes[qtype] = (self.custom_saver,self.custom_restore)
            self.alltypes.update(self.custypes)
            
        if qtype not in self.alltypes: # posera pbm si modification d'une classe WARNING
            if not isinstance(queuer.__dict__,dict):
                raise TypeError("A custom class must have a __dict__ attribute to be saved.\nPlease set customs adapters and converters to save your object")
            self.create_custom_class(qtype,queuer)
            
        return self.alltypes[qtype][0](queuer)
    
    def create_table_dict(self,model):
        """The model is a BaseDict with every key inside,
        and value with correct type"""
        keys = list(sorted(model.keys()))
        table_name = model.name
        logger.debug(model.values())
        command = """CREATE TABLE "{}"(id INTEGER PRIMARY KEY, {});""".format(
            table_name,', '.join([key+' '+ self.storing_type(type(model[key])) for key in keys])
        )
        self.execute(command)
        
    def create_custom_class(self,qtype,model):
        """Creates a custom class :
        save name of the class, the module in which it is
        creates a table with the attributes"""
        attributes = slaves.BaseDict(type_of(model).__name__,**model.__dict__.copy())
        # setting special attributes
        ## creating lazy attributes
        if 'lazy_objects' in model.__dir__():
            for lazy_thing in model.lazy_objects():
                attributes[lazy_thing] = slaves.Lazy(value = attributes[lazy_thing])
        ## creating BaseDict
        if 'basedict_objects' in model.__dir__():
            for basedict_thing in model.basedict_objects():
                attributes[basedict_thing] = slaves.BaseDict(basedict_thing,attributes[basedict_thing])
        ## not counting some attributes
        if 'not_to_be_saved' in model.__dir__():
            for key in model.not_to_be_saved():
                del(attributes[key])
        # create table
        self.create_table_dict(attributes)
        
        # update custypes table
        primekey = self.get_new_id('custypes')
        self.execute("""INSERT INTO custypes VALUES (?, ?, ?);""",
                     (primekey,qtype.__name__,qtype.__module__))
        
        # adding class into custypes
        self.custypes[qtype] = (self.custom_saver,self.custom_restore)
    
    def custom_saver(self,obj):
        """Sauvegarde les attributs dans la table prévue à cet effet.
        vérifier les attributs. Fait appel à saver si attribut n'est pas un int"""
        if '_regex' in obj.__dict__:
            for key,value in obj._regex:
                obj._regex[key] = [slaves._Regex(item) for item in value ]
            for key,value in obj.regex:
                obj.regex[key] = [slaves.Regex(item) for item in value ]
        
        if 'lazy_objects' in obj.__dir__():
            for lazy_thing in obj.lazy_objects():
                obj[lazy_thing] = slaves.Lazy(value = obj[lazy_thing])
                
        if 'not_to_be_saved' in obj.__dir__():
            for key in obj.not_to_be_saved():
                del(obj.__dict__[key])
                
        if 'basedict_objects' in obj.__dir__():
            for basedict_thing in obj.basedict_objects():
                obj.__dict__[basedict_thing] = slaves.BaseDict(basedict_thing,obj.__dict__[basedict_thing])
                
        table_name = type_of(obj).__name__
        attributes = slaves.BaseDict(table_name,**obj.__dict__.copy())
        assert obj.__dict__ is not attributes 
        id, *useless_thing = self.adapters.adapt_BaseDict(attributes).partition('|')
        return id
    
    def _load_module(self,module):
        """Load modules to load classes
        module : str"""
        if module not in self.loaded_modules:
            self.loaded_modules[module] = importlib.import_module(module)
        return self.loaded_modules[module]
    
    def _load_class(self,classe,module=None):
        """Load class"""
        modules_to_load = [self._load_module,lambda x:builtins]
        module = modules_to_load[not module](module)
        logger.debug(classe)
        return getattr(module,classe)
    
    def _type_manager(self,type_entered=None,string_entered=None):
        """Manages types to save them as strings
        or return type from string as following:
        module@type"""
        if type_entered:
            return "{}@{}".format(type_entered.__module__,type_entered.__name__)
        logger.debug(string_entered)
        module, classe = string_entered.split("@")
        return self._load_class(classe,module)
    
    def type_as_string(self,obj):
        """Return type of obj as a string :
        module@type"""
        return self._type_manager(type_of(obj))
        
    def storing_type(self, type_entered):
        """Return if the type must be saved as 
        TEXT, REAL, INTEGER or BLOB
        """
        match = {
            int:"INTEGER",
            float:"REAL",
            bytes:"BLOB",
            }
        return match.get(type_entered,"TEXT")
        
    
    def restore(self,**request):
        """restore objects matching with request.
        return a list of these objects.
        each named arg is the attribute of the object,
        and the value its value : example :
        self.restore(ordo=1962,propre='romanus') return
        all objects with ordo and propre attributes,
        and whose ordo == 1962, and propre == 'romanus'"""
        pass
    
    def custom_restore(self,data_entered,qtype):
        """Restore a custom object entered"""
        logger.debug(data_entered)
        self.update_custypes(qtype)
        returned_obj = qtype()
        attributes = self.adapters.convert_BaseDict('{}|{}'.format(data_entered,qtype.__name__))
        returned_obj.__dict__.update(attributes)
        return returned_obj

    
    def _restore(self,data_entered,qtype):
        """Restore data. qtype is a type object."""
        
        self.update_custypes(qtype)
        if qtype in self.custypes:
            returned_value = self.custom_restore(data_entered,qtype)
        else:
            returned_value = self.alltypes[qtype][1](data_entered)
        return returned_value
    
    def _restore_from_string(self,string_entered):
        """Restore data from a string with following
        structure : data/module@type"""
        if not isinstance(string_entered,str):
            return string_entered
        str_data, sep, str_type = string_entered.rpartition('/')
        type_of_data = self._type_manager(string_entered=str_type)
        logger.debug(string_entered)
        logger.debug(str_data)
        logger.debug(type_of_data)
        return self._restore(str_data,type_of_data)
    
    def update_custypes(self,qtype):
        """Change tuples in custypes to type"""
        if (qtype.__name__,qtype.__module__) in self.alltypes:
            del(self.custypes[(qtype.__name__,qtype.__module__)])
            self.custypes[qtype] = (self.custom_saver,self.custom_restore)

        
        
        
                
        
        
