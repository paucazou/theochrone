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

import builtins
import importlib
import os
import sqlite3
from programme import phlog
logger = phlog.loggers['console']

# Functions
## lambdas
long_or_short = lambda string : [ShortStr,LongStr][len(string)>150](string)

## classic
def type_of(item):
    """Return type of item
    if item = str, return LongStr or ShortStr"""
    if isinstance(item,str):
        item = long_or_short(item)
    return type(item)
    

# Classes
        
class ShortStr(str):
    """A string whith len <= 150"""
    def __init__(self,value):
        if len(value) > 150:
            raise ValueError("Length of string is greater than 150") # essayer de renvoyer un LongStr et vice versa TODO
        str.__init__(self)
        
class LongStr(str):
    """A string whith len > 150"""
    def __init__(self,value):
        if len(value) <= 150:
            raise ValueError("Length of string is lower or equal to 150")
        str.__init__(self)
        
builtins.ShortStr = ShortStr
builtins.LongStr = LongStr

class DBManager():
    """Manages the database"""
    
    def __init__(self,base,are_attributes_not_to_be_saved=True):
        """base is a pathlike object"""
        if not os.path.isfile(base):
            already_exists = False
        else:
            already_exists = True
        self._base_path = base
        self.are_attributes_not_to_be_saved = are_attributes_not_to_be_saved # useful for write only
        self.connect()
        self.cursor = self.db.cursor()
        if not already_exists:
            self._create_main()
        self.loaded_modules = {}
        self.builtin = {
            list: self.adapt_list,
            tuple:self.adapt_list,
            dict:self.adapt_dict,
            str:self.StrManager,
            None:lambda x:x,
            int:self.adapt_int_to_str,
            bool:self.adapt_bool_to_str,
            builtins.ShortStr:self.StrManager, # WARNING dev : on ipython3, custom classes defined in this scope are no more attainable if the file is changed !!! Please future self, don't panic and simply add these lines by hand.
            builtins.LongStr:self.StrManager,
            }
        
        self.cursor.execute("""SELECT name,module FROM custypes""")
        custypes = self.cursor.fetchall()
        logger.debug(custypes)
        self.custypes = {custype:self.custom_saver for custype in custypes}
        self.alltypes = self.custypes.copy()
        self.alltypes.update(self.builtin)
        sqlite3.register_adapter(list,self.adapt_list)
        
    def __del__(self):
        self.db.close()
        
    def close(self):
        """close base and delete self"""
        self.db.close()
        
    def connect(self):
        self.db = sqlite3.connect(self._base_path)
    
    def adapt_list(self,list_entered):
        for i,item in enumerate(list_entered):
            list_entered[i] = "{}/{}".format(
                self._saver(item),
                self._type_manager(type_entered=type_of(item)) # attention, il y a des bizarreries avec ShortStr
                )
        return """[{}]""".format(','.join(list_entered))
    
    def adapt_dict(self,dict_entered):
        """Save dict and dict like"""
        logger.debug("dict_entered = {}; type : {}".format(dict_entered,type_of(dict_entered)))
        dict_type = type_of(dict_entered)
        pairs = []
        for key, value in dict_entered.items():
            pair = """{}/{}:{}/{}""".format(
                self._saver(key),self._type_manager(type_entered=type_of(key)),
                self._saver(value),self._type_manager(type_entered=type_of(value)))
            pairs.append(pair)
        return """<{}>""".format(",".join(pairs))
    
    def adapt_int_to_str(self,int_entered):
        """This method is to save int as str.
        It should not be used outside of special savers
        like adapt_dict or adapt_list"""
        return str(int_entered)
    
    def adapt_bool_to_str(self,bool_entered):
        """Method which changes a bool to
        its numeric value, and return it as a str"""
        return str(int(bool_entered))
        
    def _create_main(self): # TODO faire une table pour les images ?
        """Creates a virgin base with a main table.
        main table consists in an ID, a name and and a type columns.
        The ID of the main object is the same in the whole database.
        The custypes is the table of custom types to which refers the type column of the main table"""
        self.execute("""CREATE TABLE main(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type INTEGER);""") # is main useless ?
        self.execute("""CREATE TABLE custypes(
            id INTEGER PRIMARY KEY,
            name TEXT,
            module TEXT,
            types TEXT);""")
        self.execute("""CREATE TABLE ShortStr( 
            id INTEGER PRIMARY KEY,
            text TEXT);""") # for strings <= 150
        self.execute("""CREATE TABLE LongStr(
            id INTEGER PRIMARY KEY,
            text TEXT);""") # for strings > 150
        
    def _str_manager(self,item,table_name):
        """Save strings"""
        self.execute("""SELECT id FROM {} WHERE text = ?;""".format(table_name),(item,))
        try:
            id = self.cursor.fetchone()[0]
            logger.debug(id)
        except TypeError:
            id = self.get_new_id(table_name)
            self.execute("""INSERT INTO {} VALUES (?,?);""".format(table_name),(id,item))
        return id  
    
    def StrManager(self,item):
        """Save strings"""
        tables = ['ShortStr','LongStr']
        is_long = len(item) > 150
        return self._str_manager(item,tables[is_long])
        
        
    def execute(self,*command):
        """Executes the command (any SQL command)
        Commits just after"""
        logger.debug(command)
        self.cursor.execute(*command)
        self.db.commit()
        
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
            self.custypes[qtype] = self.custom_saver
            self.alltypes.update(self.custypes)
            
        if qtype not in self.alltypes: # posera pbm si modification d'une classe WARNING
            assert isinstance(queuer.__dict__,dict)
            self.create_custom_class(qtype,queuer)
            
        return self.alltypes[qtype](queuer)
    
    def create_custom_class(self,qtype,model): # 
        """Creates a custom class :
        save name of the class, the module in which it is (how ?)
        creates a table with the attributes"""

        # creating class table
        keys = list(sorted(model.__dict__.keys()))
        ## not counting some attributes
        if self.are_attributes_not_to_be_saved:
            keys = [ key for key in keys if key not in model.not_to_be_saved() ]
        ## iterating over attributes
        command = """CREATE TABLE {}( id INTEGER PRIMARY KEY, {});""".format(
            qtype.__name__, ', '.join([key + self.storing_type(type_of(model.__dict__[key])) for key in keys])
            )
        self.execute(command)
        ## set attributes types
        type_keys = {}
        for key in keys:
            type_keys[key] = self._type_manager(type_entered=type_of(model.__dict__[key]))
            
        types = '|'.join(
            [key+'/'+value for key, value in type_keys.items() ])
        primekey = self.get_new_id('custypes')
        self.execute("""INSERT INTO custypes VALUES (?, ?, ?, ?);""",
                     (primekey,qtype.__name__,qtype.__module__,types))
        
        # adding class into custypes
        self.custypes[qtype] = self.custom_saver
        self.alltypes.update(self.custypes)
    
    def custom_saver(self,obj):
        """Sauvegarde les attributs dans la table prévue à cet effet.
        vérifier les attributs. Fait appel à saver si attribut n'est pas un int"""
        table_name = type(obj).__name__
        attributes = obj.__dict__.copy() # supprimer à ce moment les attributs rejetés TODO
        assert obj.__dict__ is not attributes 
        primekey = self.get_new_id(table_name)
        # get the columns names 
        #column_info = self.execute('SELECT * FROM {}'.format(table_name))
        #columns = list(map(lambda x : x[0], column_info.description)) # a list with the column names
        types = self.get_columns_nt(table_name)
        columns = dict(item.split('/') for item in types.split('|'))
        columns = { key : self._type_manager(string_entered=value) for key, value in columns.items()}
        logger.debug(columns)
        for key,value in attributes.items():
            if key in columns and not isinstance(value,int) and not isinstance(value,bytes): # utiliser la liste des types
                item_type = columns[key]
                if not type_of(value) == item_type:
                    raise TypeError("Attribute entered has not required type for this class :\ntype: {}\nvalue: {} has type: {}".format(item_type,value,type(value)))
                attributes[key]=self._saver(value)
        values = [primekey] + [ val for key,val in sorted(attributes.items()) ]
        command = """INSERT INTO {} VALUES ({}?);""".format(table_name,"?, "*(len(values) -1))
        self.execute(command,values) # TODO voir si on ne peut pas utiliser plutôt un dict, qui serait plus commode
        return primekey
    
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
        module%#@type"""
        if type_entered:
            return "{}@{}".format(type_entered.__module__,type_entered.__name__)
        module, classe = string_entered.split("@")
        return self._load_class(classe,module)
        
    def storing_type(self, type_entered):
        """Return if the type must be saved as 
        TEXT, INTEGER or BLOB
        """
        as_text = (list,tuple,dict)
        if type_entered in as_text:
            sqtype = "TEXT"
        elif isinstance(type_entered,bytes):
            sqtype = "BLOB"
        else:
            sqtype = "INTEGER"
        return " " + sqtype
    
    def restore(self,**request):
        """restore objects matching with request.
        return a list of these objects.
        each named arg is the attribute of the object,
        and the value its value : example :
        self.restore(ordo=1962,propre='romanus') return
        all objects with ordo and propre attributes,
        and whose ordo == 1962, and propre == 'romanus'"""
        pass
        
        
                
        
        
