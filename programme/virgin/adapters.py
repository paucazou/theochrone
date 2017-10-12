#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the converters and adapters
for virgindb."""
import phlog
import virgin.slaves as slaves
# global paramaters
logger = phlog.loggers['console']
first_bounds='[<'
second_bounds='>]' # to parse lists and dicts.
str_like_classes = ('ShortStr','LongStr','_Regex','Regex')

# functions

## lambda
long_or_short = lambda string : [slaves.ShortStr,slaves.LongStr][len(string)>150](string)

def type_of(item):
    """Return type of item
    if item = str, return LongStr or ShortStr"""
    if isinstance(item,str):
        item = long_or_short(item)
    return type(item)

def bytes_to_str(string_entered):
    """Change string_entered to str
    if string_entered is a bytes string"""
    if isinstance(string_entered,bytes):
        string_entered = string_entered.decode()
    return string_entered

def parse_list(string_entered,first_bounds=first_bounds,second_bounds=second_bounds):
    """Split a string into a list
    Protects lists or dicts if there are inside it""" # TODO voir s'il ne vaut pas mieux utiliser ast.literal_eval
    logger.debug(string_entered)
    list_returned = []
    item = ""
    level = 0
    for char in string_entered[1:-1]:
        if char in first_bounds:
            level += 1
        elif char in second_bounds:
            level -= 1
        elif level < 1 and char == ",":
            list_returned.append(item)
            char = ""
            item = ''
        item += char
    list_returned.append(item) # for the last item
    return list_returned
    
def parse_dict(string_entered,first_bounds=first_bounds,second_bounds=second_bounds):
    """Similar to parse_list, except
    that this one is for dict"""
    dict_returned = {}
    level = 0
    temp_item = ''
    key = ''
    for char in string_entered[1:-1]:
        if char in first_bounds:
            level += 1
        elif char in second_bounds:
            level -= 1
        elif level < 1 and char == ':':
                key = temp_item
                temp_item = ''
                char = ''
        elif level < 1 and char == ',':
                dict_returned[key] = temp_item
                temp_item = ''
                char = ''
        temp_item += char
    dict_returned[key] = temp_item
    return dict_returned    

def converter_factory(class_name):
    """Return a function : a converter for string like objects"""
    def converter(self,id_entered):
        return self.convert_str(id_entered,class_name)
    return converter

# classes

class Adapter:
    """This class contains methods
    used by DBManager to adapt and convert
    object to and from a database"""
    
    
    def __init__(self,dbmanager):
        self.dbmanager = dbmanager
        
    # adapters / converters 
    ## Lazy
    def adapt_Lazy(self,lazy_thing):
        """Adapt a lazy object to save it into db"""
        return """lazy({}/{})""".format(
            self.dbmanager._saver(lazy_thing.value),
            self.dbmanager._type_manager(type_entered=type_of(lazy_thing.value))
            )
    
    def convert_Lazy(self,string_entered):
        """Convert a string_entered into a Lazy object"""
        raw_data=string_entered.replace("lazy(","").replace(")","")
        return slaves.Lazy(db=self.dbmanager,
                    raw_data = raw_data,
                    )
    
    ## str
    def adapt_str(self,string_entered):
        table_name = type_of(string_entered).__name__
        logger.debug('On y est')
        self.dbmanager.execute("""SELECT id FROM {} WHERE text = ?;""".format(table_name),(string_entered,))
        logger.debug('And here too')
        try:
            id = self.dbmanager.cursor.fetchone()[0]
            logger.debug(id)
        except TypeError:
            id = self.dbmanager.get_new_id(table_name)
            self.dbmanager.execute("""INSERT INTO {} VALUES (?,?);""".format(table_name),(id,string_entered))
        return id 
        
    def convert_str(self,id_entered,table_name=None):
        if not table_name:
            raise ValueError("A table name must be entered.")
        return self.dbmanager.fetchone("""SELECT text FROM {} WHERE id = ?;""".format(table_name),(id_entered,))[0]
    
    ## bool
    def adapt_bool(self,bool_entered):
        return int(bool_entered)
    
    def convert_bool(self,int_entered):
        return bool(int(int_entered))
    
    # None
    def adapt_None(self,None_entered):
        return 'None'
    
    def convert_None(self,string_entered):
        return None
    
    #int
    def adapt_int(self,int_entered):
        return self.dbmanager.adapt_int_to_str(int_entered)
    
    def convert_int(self,string_entered):
        return self.dbmanager.adapt_int_to_str(string_entered,restore=True)
    
    # dict
    def adapt_dict(self,dict_entered):
        pairs = []
        for key, value in dict_entered.items():
            pair = """{}/{}:{}/{}""".format(
                self.dbmanager._saver(key),self.dbmanager._type_manager(type_entered=type_of(key)),
                self.dbmanager._saver(value),self.dbmanager._type_manager(type_entered=type_of(value)))
            pairs.append(pair)
        return """<{}>""".format(",".join(pairs))
    
    def convert_dict(self,string_entered):
        string_entered = bytes_to_str(string_entered)
        dict_tmp = parse_dict(string_entered)
        logger.debug(dict_tmp)
        new_dict = {}
        for key,value in dict_tmp.items():
            new_dict[self.dbmanager._restore_from_string(key)] = self.dbmanager._restore_from_string(value)
        return new_dict
    
    ## BaseDict
    def adapt_BaseDict(self,dict_entered):
        """dict_entered must be a slaves.BaseDict"""
        if not self.dbmanager.fetchone("SELECT name FROM sqlite_master WHERE TYPE='table' AND NAME=?;",(dict_entered.name,)):
            self.dbmanager.create_table_dict(dict_entered)
        id = self.dbmanager.save_row(dict_entered.name,[value for key, value in sorted(dict_entered.items())])
        return "{}|{}".format(id,dict_entered.name)
    
    def convert_BaseDict(self,string_entered):
        id,sep,table_name = string_entered.partition('|')
        tmp_dico = self.dbmanager.restore_row(table_name,dict,id=int(id))[0]
        del(tmp_dico['id'])
        return tmp_dico
    
    # list
    def adapt_list(self,list_entered):
        for i,item in enumerate(list_entered):
            list_entered[i] = "{}/{}".format(
                self.dbmanager._saver(item),
                self.dbmanager._type_manager(type_entered=type_of(item))
                ) 
        returned_value = """[{}]""".format(','.join(list_entered))
        logger.debug(returned_value)
        return returned_value
    
    def convert_list(self,string_entered):
        string_entered = bytes_to_str(string_entered)
        list_tmp = parse_list(string_entered)
        new_list = []
        for elt in list_tmp:
            new_list.append(self.dbmanager._restore_from_string(elt))
        return new_list
    
    ## tuple
    def convert_tuple(self,string_entered):
        return tuple(self.convert_list(string_entered))
                     
# creating converters for string_like classes
for class_name in str_like_classes:
    method_name = 'convert_' + class_name
    setattr(Adapter,method_name,converter_factory(class_name))
    
        
