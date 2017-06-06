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
from PyQt5.QtCore import QCoreApplication, Qt, QTranslator
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox, QLabel, QVBoxLayout, QWidget

_ = QCoreApplication.translate

class SettingsWindow(QWidget,SuperTranslator):
    """Settings window"""
    def __init__(self):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        
        self.initUI()
        self.retranslateUI()
    
    def initUI(self):
        #title
        title_font = QFont()
        title_font.setPointSize(20)
        self.title = QLabel('Settings')
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignHCenter)
        # Main checkbox
        self.settings_state = QCheckBox('Set settings off',self)
        self.settings_state.toggle()
        self.settings_state.stateChanged.connect(self.SettingState)
        if not officia.pdata():
            self.settings_state.setChecked(False)
        else:
            self.settings_state.setChecked(True)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.settings_state)
        self.setLayout(self.layout)
        self.show()
        
    def retranslateUI(self):
        self.setWindowTitle(_("SettingsWindow","Settings"))
        if self.settings_state.isChecked():
            self.settings_state.setText(_("SettingsWindow","Set settings OFF"))
        else:
            self.settings_state.setText(_("SettingsWindow","Set settings ON"))
        
    def SettingState(self, state):
        if state == Qt.Checked:
            officia.pdata(SET='ON')
        else:
            officia.pdata(SET='OFF')
        self.retranslateUI()
