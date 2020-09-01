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
import officia

from configparser import ConfigParser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlListProperty
from PyQt5.QtCore import pyqtSlot, pyqtSignal, pyqtProperty, QVariant, QAbstractListModel, QModelIndex, Qt, QTranslator, QObject, QCoreApplication

# QML Resources
import qml_rcc

# a set of years from 1600 to 4100
comboYears = list(range(1600,4100))

# set all available language, using for Settings and SearchPage
list_lang = ["Roman","Australian","American","Brazilian","Canadian","English","French","New-Zealander","Polish","Portugese","Scottish","Spanish","Welsh"]

# a set of month, using for SearchPage
list_month = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)

        # Install translator
        self.translator = QmlTranslator(self)

        # set QML engine
        self.engine = QQmlApplicationEngine()

        # Communication with QML
        self.engine.rootContext().setContextProperty("translator", self.translator)
        self.engine.rootContext().setContextProperty("comboYears", comboYears)
        self.engine.rootContext().setContextProperty("listLang", list_lang)
        self.engine.rootContext().setContextProperty("listMonth", list_month)

        # Set the calendar on the main page
        self.settings = Settings()
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

        # Separate nameFest and typeFest
        list_str = str(self.lfeast[index]).split(",")
        if len(list_str) == 1:
            list_str += list_str[0]

        # Select the good icon
        color = self.lfeast[index].couleur
        if color == "blanc":
            icon_path = "qrc:/images/icons/saint_gold.png"
        elif color == "vert":
            icon_path = "qrc:/images/icons/saint_green.png"
        elif color == "rose":
            icon_path = "qrc:/images/icons/saint_pink.png"
        elif color == "violet":
            icon_path = "qrc:/images/icons/saint_purple.png"
        elif color == "rouge":
            icon_path = "qrc:/images/icons/saint_red.png"
        elif color == "noir":
            icon_path = "qrc:/images/icons/saint_black.png"
        else:
            icon_path = "qrc:/images/icons/saint.png"

        # Fill all data in a dict about the fest
        self.dictio["nameFest"] = list_str[0]
        self.dictio["typeFest"] = list_str[1]
        self.dictio["srcImg"] = icon_path
        self.dictio["srcImgSaint"] = "qrc:/images/background/default_image_saint.png"
        self.dictio["proper"] = str(self.lfeast[index].propre).capitalize()
        self.dictio["edition"] = str(self.lfeast[index].ordo)
        self.dictio["celebration"] = str(self.lfeast[index].celebree).capitalize()
        self.dictio["classe"] = str(self.lfeast[index].degre)
        self.dictio["liturgicalColor"] = str(self.lfeast[index].couleur).capitalize()
        self.dictio["temporal"] = str(self.lfeast[index].temporal).capitalize()
        self.dictio["sanctoral"] = str(self.lfeast[index].sanctoral).capitalize()
        self.dictio["liturgicalTime"] = officia.affiche_temps_liturgique(self.lfeast[index]).capitalize()
        self.dictio["transferredFest"] = str(self.lfeast[index].transferee).capitalize()
        self.dictio["massText"] = self.lfeast[index].link
        return self.dictio

    @pyqtSlot(int, result=QVariant)
    def checkPal(self, index):
        if self.lfeast[index].pal == True:
            return False
        else:
            return True

    changeSignal = pyqtSignal(QVariant)
    @pyqtSlot(int, int, int)
    def changeDate(self, year, month, day):
        self.lcalendar(datetime.date.today().year)
        self.lfeast = self.lcalendar[datetime.date(year, month, day)]
        self.nbElements = len(self.lfeast)
        self.changeSignal.emit(self.lcalendar)  # enable to update feast in QML

class QmlTranslator(QObject):
    def __init__(self, app):
        QObject.__init__(self)
        self.app = app
        self.mTranslator = QTranslator()
        self.updateLanguage("EN")


    @pyqtSlot(str)
    def updateLanguage(self, lang):
        if lang == "EN":
            self.mTranslator.load("Theochrnone_en_EN.qm", "i18n")
            self.app.installTranslator(self.mTranslator)
        elif lang == "FR":
            self.mTranslator.load("Theochrone_fr_FR.qm", "i18n")
            self.app.installTranslator(self.mTranslator)
        else:
            self.app.removeTranslator(self.mTranslator)
            print("removed translator")



class Settings(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.filePath = "gui_mobile/.settings.ini"
        self.list_settings = ['','']
        self.getSettings()

    def getSettings(self):
        if os.path.isfile(self.filePath):
            file = ConfigParser()
            file.read("gui_mobile/.settings.ini")
            self.list_settings[0] = file.get('settings', 'language')
            self.list_settings[1] = file.get('settings', 'proper')
        else:
            return