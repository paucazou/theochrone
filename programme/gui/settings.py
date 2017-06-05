#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import os.path
import sys
chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/..')
sys.path.append(programme)
sys.path.append(chemin)
import officia
os.chdir(chemin)
from translation import *
from PyQt5.QtCore import QCoreApplication, QTranslator
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QWidget

_ = QCoreApplication.translate

class SettingsWindow(QWidget,SuperTranslator):
    """Settings window"""
    def __init__(self):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        
        self.initUI()
        self.retranslateUI()
        self.show()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        self.settings_on = QCheckBox('Set settings off',self)
        self.layout.addWidget(self.settings_on)
        self.setLayout(self.layout)
        
    def retranslateUI(self):
        self.setWindowTitle = _("SettingsWindow","Settings")
        self.settings_on.setText(_("SettingsWindow","Set settings on/off"))
