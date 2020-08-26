#!/usr/bin/python3
# -*-coding:Utf-8 -*
# Deus in adjutorium meum intende

import sys
import datetime
import os.path
chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/..')
sys.path.append(programme)
sys.path.append(chemin)
import annus

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlListProperty
from PyQt5.QtCore import pyqtSlot, pyqtProperty, QAbstractListModel, QModelIndex, Qt, QTranslator, QObject, QCoreApplication
from translation import *

# QML Resources
import qml_rcc

# a set of years from 1600 to 4100
comboYears = list(range(1600,4100))

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

        # Communication with QML
        self.engine.rootContext().setContextProperty("comboYears", comboYears)

        self.lcalendar = annus.LiturgicalCalendar(proper='roman', ordo=1962)
        self.lcalendar(2020)
        self.list_feast = self.lcalendar[datetime.date.today()]
        lelements = ListElements(self.list_feast)
        self.engine.rootContext().setContextProperty("lElements", lelements)

class Main():
    def __init__(self, parent, args):
        self.parent = parent
        self.processCommandLineArgs(args)



    def processCommandLineArgs(self, args):
        args, debut, fin = args
        reverse, plus = args.INVERSE, args.plus

class ListElements(QObject):
    def __init__(self, lfeast):
        QObject.__init__(self)
        self.lfeast = lfeast
        self.nbElements = len(lfeast)
        print(self.nbElements)

    @pyqtSlot(result=int)
    def getNbElements(self):
        return self.nbElements

    @pyqtSlot(int, result=dict)
    def getData(self, index):
        self.dictio = {}
        self.dictio["nameFest"] = str(self.lfeast[index])
        self.dictio["typeFest"] = str(self.lfeast[index])
        self.dictio["srcImg"] = "qrc:/images/icons/saint_gold.png"
        self.dictio["srcImgSaint"] = "qrc:/images/background/default_image_saint.png"
        self.dictio["proper"] = self.lfeast[index].propre
        self.dictio["edition"] = "1962"
        self.dictio["celebration"] = str(self.lfeast[index].celebree)
        self.dictio["classe"] = str(self.lfeast[index].degre)
        self.dictio["liturgicalColor"] = self.lfeast[index].couleur
        self.dictio["temporal"] = str(self.lfeast[index].temporal)
        self.dictio["sanctoral"] = str(self.lfeast[index].sanctoral)
        self.dictio["liturgicalTime"] = self.lfeast[index].temps_liturgique()
        self.dictio["transferredFest"] = str(self.lfeast[index].transferee)
        self.dictio["massText"] = self.lfeast[index].link
        return self.dictio




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
