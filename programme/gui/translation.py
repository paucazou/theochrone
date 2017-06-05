#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

class ReTranslateBox():
    """A class which can contain only items with the retranslateUI function"""
    def __iter__(self):
        """Iters values of  self.__dict__"""
        for value in self.__dict__.values():
            yield value
        
    def __repr__(self):
        """Returns self.__dict__ to be recognized in the interactive interpreter"""
        return str(self.__dict__)
    
    def __setattr__(self,attribute,value):
        """Tests wether the 'value' is an object which has the function retranslateUI in it.
        If it is true, set the 'attribute'. This function should be useless in prod."""
        if 'retranslateUI' in value.__dir__():
            self.__dict__[attribute] = value
        else:
            raise TypeError("""Could not set attribute '{}' : '{}' object doesn't contain any 'retranslateUI' method.""".format(attribute,value))
        
class SuperTranslator():
    """A class which should be inherited by every custom widget class to make an easy translation on the fly."""
    
    def __init__(self):
        """This method only defines a ReTranslateBox object which is called 'W'. This attribute can only store widgets with a 'retranslateUI' method, i.e. from objects which inherit of this class"""
        self.W = ReTranslateBox()
        
    def retranslateUI(self):
        """This method calls every 'retranslateUI' methods of the 'W' attribute.
        This method should be overloaded by every widget which contains
        widgets to be immediately retranslated
        (i.e., which are not custom widgets).
        User shouldn't forget to call this function if necessary in the function itself :
        SuperTranslator.retranslateUI()"""
        for a in self.W:
            a.retranslateUI()
