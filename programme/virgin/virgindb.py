#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
# This module is intented to create a virgin database with sqlite3
# Rules :
# Each class a different table
# Only numbers (integers and reals (float) are directly stored in the instance 
# texts, lists, dicts, etc. are stored as integers which points to another table,
# whose name is equal to the key : ex : 'station' key points to 'station' table.
# Lists are represented by a text value with this separator : @@@
# dicts should be reprenseted by an integer pointing to another table
# As much as possible, the database should be absolutely automated.
# The user is supposed to give an instance, and the database store it automatically,
# even if the class is not previously set, and even if the class does not yet contains new attributes.
# It should be also possible to turn away some attributes which are only useful when data are loaded,
# for instance 'date'. A list of some of these attributes should be set somewhere, probably in the class definition, or in another file
#
# instances entered by user are called 'main objects'
# all main objets have at least a reference (or are saved) in a table called 'main'. Main table is the entry of the whole database.
#
# custom savers can be created with a new class containing a get and a set methods + a __call__ method. For a similar object, more than one get and set methods can be created for a different behaviour. An __init__ method should be created then to let the script know which method use, in which case. See DictManager for an example.
# TODO faire une fonction de création de table
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
# Functions
## classic
    
def hash_n_point(string_entered):
    """Change string_entered : replace "#" by ".",
    and vice versa"""
    chars = ('#','.')
    chars = (chars,chars[::-1])
    place = '.' in string_entered
    return string_entered.replace(*chars[place])
    
# class

class DBManager(): # on change tout
    """Manages the database"""
    
    def __init__(self,base,are_attributes_not_to_be_saved=True):
        """base is a pathlike object"""
        self.adapters = adapters.Adapter(self)
        if not os.path.isfile(base):
            already_exists = False
        else:
            already_exists = True
        self._base_path = base
        self.are_attributes_not_to_be_saved = are_attributes_not_to_be_saved # useful for write only
        self.connect()
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        if not already_exists:
            self._create_main()
        self.loaded_modules = {}
        
        self.builtin = { # changer cela : un tuple (adapter,converter)
            list: (self.adapters.adapt_list,self.adapters.convert_list),
            tuple:(self.adapters.adapt_list,self.adapters.convert_tuple),
            dict:(self.adapters.adapt_dict,self.adapters.convert_dict),
            bool:(self.adapters.adapt_bool,self.adapters.convert_bool),
            slaves.ShortStr:(self.adapters.adapt_str,self.adapters.convert_ShortStr), # WARNING dev : on ipython3, custom classes defined in this scope are no more attainable if the file is changed !!! Please future self, don't panic and simply add these lines by hand.
            slaves.LongStr:(self.adapters.adapt_str,self.adapters.convert_LongStr),
            int:(self.adapters.adapt_int,self.adapters.convert_int),
            str:(self.adapters.adapt_str,self.adapters.convert_str),
            builtins.NoneType:(self.adapters.adapt_None,self.adapters.convert_None),
            }
        
        
        # registering adaptaters
        """for key, value in self.builtin.items():
            sqlite3.register_adapter(key,value[0])
            sqlite3.register_converter(key.__name__,value[1])"""
        
            
        custypes = self.fetchall("""SELECT name,module FROM custypes""")
        logger.debug(custypes)
        # registering custom converters
        for type_name, type_module in custypes:
            sqlite3.register_converter(type_name,self.custom_restore)
        self.custypes = {custype:(self.custom_saver,self.custom_restore) for custype in custypes}
        self.alltypes = collections.ChainMap(self.builtin,self.custypes)
        
    def __del__(self):
        self.db.close()
    
    def close(self):
        """close base"""
        self.db.close()
        
    def connect(self):
        self.db = sqlite3.connect(self._base_path)
    
    def deprecated_adapt_list(self,list_entered,restore=False): # DEPRECATED
        """Turn a list into text ;
        if restore == True, turn list_entered into list"""
        if restore:
            list_returned = list_entered[1,-1].split(',')
            return list_returned
        
        for i,item in enumerate(list_entered):
            list_entered[i] = "{}/{}".format(
                self._saver(item),
                self._type_manager(type_entered=type_of(item)) # attention, il y a des bizarreries avec ShortStr
                )
        return """[{}]""".format(','.join(list_entered))
    
    def adapt_dict(self,dict_entered,restore=False): # DEPRECATED
        """Save dict and dict like
        if restore == True, turn dict_entered into dict""" # WARNING et si c'est un ordered dict ???
        if restore:
            dict_returned = dict_entered[1,-1].split(',')
            return dict_returned
        
        logger.debug("dict_entered = {}; type : {}".format(dict_entered,type_of(dict_entered)))
        dict_type = type_of(dict_entered)
        pairs = []
        for key, value in dict_entered.items():
            pair = """{}/{}:{}/{}""".format(
                self._saver(key),self._type_manager(type_entered=type_of(key)),
                self._saver(value),self._type_manager(type_entered=type_of(value)))
            pairs.append(pair)
        return """<{}>""".format(",".join(pairs))
    
    def adapt_int_to_str(self,int_entered,restore=False): #DEPRECATED
        """This method is to save int as str.
        It should not be used outside of special savers
        like adapt_dict or adapt_list
        If restore == True, return int from str"""
        return (str,int)[restore](int_entered)
    
    def adapt_bool_to_str(self,bool_entered,restore=False): # DEPRECATED
        """Method which changes a bool to
        its numeric value, and return it as a str
        if restore == True, return bool from a str (1 or 0)"""
        return (str,bool)[restore](int(bool_entered))
        
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
        
    def create_table(self, table_name, items):
        """Create a new table.
        table_name : string
        items : sequence of sequences of two items : name (str) and type
        do not include id in items : it is already created by this method
        example : self.create_table('customers',(('name',str),('age',int),('basket',list)))"""
        values = ','.join(["{} {}".format(name,self.storing_type(qtype)) for name, qtype in items ])
        command = """CREATE TABLE {} (
        id INTEGER PRIMARY KEY,
        {});""".format(table_name,values)
        for name, qtype in items:
            self.update_custypes(qtype)
        self.execute(command)
        
    def save_row(self, table_name,data,id=0): # TODO update data
        """Save a row into a table.
        If row (ie, id) already exist, update it
        else insert data with last id
        table_name : string
        data : sequence of objects without id ; must be in the right order
        id : int"""
        laine = len(data) # laine in french has similar pronunciation to len in globish : funny, isn't it ?
        if not id:
            id = self.get_new_id(table_name)
            for i, elt in enumerate(data):
                if type(elt) not in base_types:
                    data[i] = "{}/{}".format(self._saver(elt),self._type_manager(type_entered=type_of(elt)))
            data.insert(0,id)
            command = """INSERT INTO {} values ({}?);""".format(table_name,"?, " * laine)
        self.execute(command,data)
        
    def restore_row(self,table_name,returned_type=dict,**where): # TODO ajouter les différents opérateurs
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
            tmp_container = {}
            for key,value in dict(row_object).items():
                if type(value) not in base_types:
                    value = self._restore_from_string(value)
                tmp_container[key] = value
            
            if returned_type is not dict:
                tmp_container = returned_type(tmp_container.values())
            returned_list.append(tmp_container)
        return returned_list
        
        
    def _str_manager(self,item,table_name): # DEPRECATED
        """Save strings"""
        self.execute("""SELECT id FROM {} WHERE text = ?;""".format(table_name),(item,))
        try:
            id = self.cursor.fetchone()[0]
            logger.debug(id)
        except TypeError:
            id = self.get_new_id(table_name)
            self.execute("""INSERT INTO {} VALUES (?,?);""".format(table_name),(id,item))
        return id  
    
    def StrManager(self,item,str_type=None,restore=False): # DEPRECATED
        """Save strings
        if restore == True, restore strings
        str_type is useful to restore strings.
        It can be either ShortStr or LongStr"""
        if restore:
            self.execute("""SELECT text FROM {} WHERE id = ?;""".format(str_type.__name__),(item,))
            return self.cursor.fetchone()[0]
        tables = ['ShortStr','LongStr']
        is_long = len(item) > 150
        return self._str_manager(item,tables[is_long])        
        
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
        self.execute("SELECT max(id) FROM {}".format(table_name))
        return self.cursor.fetchone()[0]
    
    def get_new_id(self,table_name):
        """A method to get the last id + 1"""
        last_id = self.get_last_id(table_name)
        return last_id + 1 if last_id else 1
    
    def get_columns_nt(self,name):
        """A method to get the columns names and the types (nt)
        from custypes"""
        self.execute("SELECT types FROM custypes WHERE name = ?;",(name,))
        return self.cursor.fetchone()[0]
        
    def saver(self,*queue):
        """Save the objects in the database
        return list of ids"""
        ids = []
        for queuer in queue:
            ids.append(self._saver(queuer))
        return ids
    
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
            assert isinstance(queuer.__dict__,dict)
            self.create_custom_class(qtype,queuer)
            
        return self.alltypes[qtype][0](queuer)
    
    def create_custom_class(self,qtype,model):
        """Creates a custom class :
        save name of the class, the module in which it is (how ?)
        creates a table with the attributes"""
        # creating class table
        
        # creating lazy attributes
        if 'lazy_objects' in model.__dir__():
            for lazy_thing in model.lazy_objects():
                model[lazy_thing] = slaves.Lazy(value = model[lazy_thing])

        
        keys = list(sorted(model.__dict__.keys()))
        ## not counting some attributes
        if self.are_attributes_not_to_be_saved:
            keys = [ key for key in keys if key not in model.not_to_be_saved() ]
        table_name =  self._type_manager(qtype)
        ## iterating over attributes
        command = """CREATE TABLE "{}"( id INTEGER PRIMARY KEY, {});""".format(
            table_name, ', '.join([key +' '+ type_of(model.__dict__[key]).__name__ for key in keys])
            ) # "" around table name are necessary to allow characters like #,., etc.
        self.execute(command)
        """## set attributes types
        type_keys = {}
        for key in keys:
            type_keys[key] = self._type_manager(type_entered=type_of(model.__dict__[key]))
            
        types = '|'.join(
            [key+'/'+value for key, value in type_keys.items() ])"""
        primekey = self.get_new_id('custypes')
        self.execute("""INSERT INTO custypes VALUES (?, ?, ?);""",
                     (primekey,qtype.__name__,qtype.__module__))
        
        # adding class into custypes
        self.custypes[qtype] = (self.custom_saver,self.custom_restore)
        self.add_custom_converter_and_adapter(qtype)
    
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
                obj[lazy_thing] = slaves.Lazy(value = model[lazy_thing])
                
        table_name = self._type_manager(type_entered=type_of(obj))
        attributes = obj.__dict__.copy() # supprimer à ce moment les attributs rejetés TODO
        assert obj.__dict__ is not attributes 
        primekey = self.get_new_id(table_name)
        # get the columns names 
        #column_info = self.execute('SELECT * FROM {}'.format(table_name))
        #columns = list(map(lambda x : x[0], column_info.description)) # a list with the column names
        """types = self.get_columns_nt(table_name)
        columns = dict(item.split('/') for item in types.split('|'))
        columns = { key : self._type_manager(string_entered=value) for key, value in columns.items()}
        logger.debug(columns)
        for key,value in attributes.items():
            if key in columns and not isinstance(value,int) and not isinstance(value,bytes): # utiliser la liste des types
                item_type = columns[key]
                if not type_of(value) == item_type:
                    raise TypeError("Attribute entered has not required type for this class :\ntype: {}\nvalue: {} has type: {}".format(item_type,value,type(value)))
                attributes[key]=self._saver(value)"""
        values = [primekey] + [ val for key,val in sorted(attributes.items()) ]
        command = """INSERT INTO {} VALUES ({}?);""".format(table_name,"?, "*(len(values) -1))
        self.execute(command,values) # TODO voir si on ne peut pas utiliser plutôt un dict, qui serait plus commode
        return """{}/{}""".format(primekey,table_name)
    
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
        return match.setdefault(type_entered,"TEXT")
        
    
    def restore(self,**request):
        """restore objects matching with request.
        return a list of these objects.
        each named arg is the attribute of the object,
        and the value its value : example :
        self.restore(ordo=1962,propre='romanus') return
        all objects with ordo and propre attributes,
        and whose ordo == 1962, and propre == 'romanus'"""
        pass
    
    def custom_restore(self,data_entered):
        """Restore a custom object entered"""
        obj_id, useless_sep, table_name = data_entered.partition('/')
        qtype = self._type_manager(string_entered=table_name)
        self.update_custypes(qtype)
        returned_obj = qtype()
        attributes = dict(
            self.fetchone("""SELECT * FROM {} WHERE id = ?;""".format(table_name),(int(obj_id),)
                          ))
        returned_obj.__dict__.update(attributes)
        return returned_obj

    
    def _restore(self,data_entered,qtype):
        """Restore data. qtype is a type object."""
        
        self.update_custypes(qtype)
            
        return self.alltypes[qtype][1](data_entered)
    
    def _restore_from_string(self,string_entered):
        """Restore data from a string with following
        structure : data/module@type"""
        str_data, sep, str_type = string_entered.rpartition('/')
        type_of_data = self._type_manager(string_entered=str_type)
        logger.debug(string_entered)
        logger.debug(str_data)
        return self._restore(str_data,type_of_data)
    
    def update_custypes(self,qtype):
        """Change tuples in custypes to type"""
        if (qtype.__name__,qtype.__module__) in self.alltypes:
            del(self.custypes[(qtype.__name__,qtype.__module__)])
            self.custypes[qtype] = (self.custom_saver,self.custom_restore)
            self.add_custom_converter_and_adapter(qtype)
            
    def add_custom_converter_and_adapter(self,qtype):
        """Add converter and adapter for a custom type"""
        sqlite3.register_adapter(qtype,self.custom_saver)
        complete_name = qtype.__module__ + '.' + qtype.__name__ # WARNING ne fonctionnera pas -> remplacer par module@type
        sqlite3.register_converter(complete_name,self.custom_restore)
        
    
        
        
        
        
                
        
        
