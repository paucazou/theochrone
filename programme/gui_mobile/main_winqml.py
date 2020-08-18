#!/usr/bin/python3
# -*-coding:Utf-8 -*
# Deus in adjutorium meum intende

import sys
import os.path
chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/..')
sys.path.append(programme)
sys.path.append(chemin)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import pyqtSlot, pyqtProperty, QAbstractListModel, QModelIndex, Qt, QTranslator, QObject, QCoreApplication
from translation import *

import qml
import images

_ = QCoreApplication.translate

class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)

        # set QML engine
        self.engine = QQmlApplicationEngine()
        self.engine.load(chemin + "/qml/main.qml")
        self.engine.quit.connect(App.quit)

        self.translator = QTranslator()
        self.installTranslator(self.translator)
        self.execute = Main(self,args)

class Main(SuperTranslator):
    def __init__(self, parent, args):
        SuperTranslator.__init__(self)
        self.parent = parent
        self.processCommandLineArgs(args)
        #self.settings = setSettings()

    def processCommandLineArgs(self, args):
        args, debut, fin = args
        reverse, plus = args.INVERSE, args.plus

"""
class setSettings(QObject):
    def __init__(self):
        self.lang = self._selectLanguage()
        self.proper = None

    def _selectLanguage(self):
        """



"""
class ListModel(QAbstractListModel):
    def __init__(self, data, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self._data = data

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        self._data[index.row()] = value
        self.dataChanged.emit(index, index, [role])
        return True

    @pyqtSlot(int, str, result=bool)
    def insert(self, row, value):
        return self.setData(self.createIndex(row, 0), value, Qt.EditRole)

    @pyqtSlot(str, result=bool)
    def append(self, value):
        return self.insert(self.count, value)
"""
