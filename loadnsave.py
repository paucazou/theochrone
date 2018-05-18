#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import enc

def load(path: str):
    """Load file (path) which is an xml file.
    return it with a closure in order to close
    the file and save the changes
    """
    with enc.Preferences(path) as f:
        l = f.prefs # l is probably a list
    class FileWrapper(type(l)):
        def __init__(self,data):
            super().__init__(data)
            self._data = data
            self._path = path
        
        def save(self):
            with enc.Preferences(path,'w') as f:
                f.prefs = self._data
            enc.prettyfyxml(path)

    return FileWrapper(l)
