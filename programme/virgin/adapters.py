#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the converters and adapters
virgindb."""
# global paramaters
first_bounds='[<'
second_bounds='>]' # to parse lists and dicts.

# functions

def parse_list(string_entered,first_bounds=first_bounds,second_bounds=second_bounds):
    """Split a string into a list
    Protects lists or dicts if there are inside it""" # TODO voir s'il ne vaut pas mieux utiliser ast.literal_eval
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
        return """lazy({}/{})""".format(self.dbmanager._saver(lazy_thing.value),lazy_thing.type)
    
    def convert_Lazy(self,string_entered):
        """Convert a string_entered into a Lazy object"""
        raw_data=string_entered.decode().replace("lazy(","").replace(")","")
        return slaves.Lazy(db=self.dbmanager,
                    raw_data = raw_data,
                    )
    
    ## str
    def adapt_str(self,string_entered):
        table_name = string_entered.__class__.__name__
        self.dbmanager.execute("""SELECT id FROM {} WHERE text = ?;""".format(table_name),(string_entered,))
        try:
            id = self.dbmanager.cursor.fetchone()[0]
            logger.debug(id)
        except TypeError:
            id = self.dbmanager.get_new_id(table_name)
            self.dbmanager.execute("""INSERT INTO {} VALUES (?,?);""".format(table_name),(id,string_entered))
        return id 
        
    def convert_str(self,id_entered,table_name=None): # TODO un converter principal, les autres faisant appel à lui et lui donnant une base
        if not table_name:
            raise ValueError("A table name must be entered.")
        return self.dbmanager.fetchone("""SELECT text FROM {} WHERE id = ?;""".format(table_name),(id_entered,))[0]
    
    ### LongStr
    def convert_LongStr(self,id_entered):
        return self.dbmanager.convert_str(id_entered,"LongStr")
    ### ShortStr
    def convert_ShortStr(self,id_entered):
        return self.dbmanager.convert_str(id_entered,"ShortStr")
    
    ## bool
    def adapt_bool(self,bool_entered):
        return int(bool_entered)
    
    def convert_bool(self,int_entered):
        return bool(int_entered)
    
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
    
    ## dict
    def adapt_dict(self,dict_entered):
        pairs = []
        for key, value in dict_entered.items():
            pair = """{}/{}:{}/{}""".format(
                self.dbmanager._saver(key),self.dbmanager._type_manager(type_entered=type_of(key)),
                self.dbmanager._saver(value),self.dbmanager._type_manager(type_entered=type_of(value)))
            pairs.append(pair)
        return """<{}>""".format(",".join(pairs))
    
    def convert_dict(self,string_entered):
        dict_tmp = parse_dict(string_entered[1:-1]).items()
        new_dict = {}
        for key,value in dict_tmp.items():
            new_dict[self.dbmanager._restore_from_string(key)] = self.dbmanager._restore_from_string(value)
        return new_dict
    
    ## list
    def adapt_list(self,list_entered):
        for i,item in enumerate(list_entered):
            list_entered[i] = "{}/{}".format(
                self.dbmanager._saver(item),
                self.dbmanager._type_manager(type_entered=type_of(item))
                )
        return """[{}]""".format(','.join(list_entered))
    
    def convert_list(self,string_entered):
        list_tmp = parse_list( string_entered[1:-1] )
        new_list = []
        for elt in list_tmp:
            new_list.append(self.dbmanager._restore_from_string(elt))
        return new_list
        
