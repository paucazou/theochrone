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
from PyQt5.QtCore import pyqtSlot, pyqtSignal, pyqtProperty, QVariant, QAbstractListModel, QModelIndex, Qt, QTranslator, QObject, QCoreApplication
from translation import *

# QML Resources
import qml_rcc

# a set of years from 1600 to 4100
comboYears = list(range(1600,4100))


class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)

        # set QML engine
        self.engine = QQmlApplicationEngine()

        # Communication with QML
        self.engine.rootContext().setContextProperty("comboYears", comboYears)

        # Set the calendar on the main page
        self.feast = ListElements('roman', 1962)
        self.engine.rootContext().setContextProperty("feast", self.feast)

        # Show the app
        self.engine.load(chemin + "/qml/main.qml")
        self.engine.quit.connect(App.quit)

class ListElements(QObject):
    def __init__(self, s_proper, s_ordo):
        QObject.__init__(self)
        self.lcalendar = annus.LiturgicalCalendar(proper=s_proper, ordo=s_ordo)
        self.lcalendar(datetime.date.today().year)
        self.lfeast = self.lcalendar[datetime.date.today()]
        self.nbElements = len(self.lfeast)

        # Signal load data
        self.changeSignal.emit(self.lcalendar)

    @pyqtSlot(result=int)
    def getNbElements(self):
        return self.nbElements

    @pyqtSlot(int, result=QVariant)
    def getData(self, index):
        self.dictio = {}

        # separate nameFest and typeFest
        list_str = str(self.lfeast[index]).split(",")
        if len(list_str) == 1:
            list_str += list_str[0]

        # Fill all data about the fest
        self.dictio["nameFest"] = list_str[0]
        self.dictio["typeFest"] = list_str[1]
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

    changeSignal = pyqtSignal(QVariant)
    @pyqtSlot(int, int, int)
    def changeDate(self, year, month, day):
        self.lcalendar(datetime.date.today().year)
        self.lfeast = self.lcalendar[datetime.date(year, month, day)]
        self.nbElements = len(self.lfeast)
        print(year,month,day)
        self.changeSignal.emit(self.lcalendar)  # enable to update feast in QML


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
