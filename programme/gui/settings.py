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
from PyQt5.QtWidgets import QCheckBox, QComboBox, QHBoxLayout, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget

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
            
        # History line number
        self.history_layout = QHBoxLayout()
        self.history_lines = QSpinBox()
        self.history_lines.setMinimum(0)
        self.history_lines.setMaximum(1000)
        self.history_lines.setValue(officia.pdata(history_info=True))
        self.history_label = QLabel('Maximum number of lines of your history')
        self.history_layout.addWidget(self.history_lines)
        self.history_layout.addWidget(self.history_label)
        
        # Language choice
        self.language_layout = QHBoxLayout()
        self.language_combo = QComboBox()
        self.languages_label = QLabel('Choose your default language')
        self.language_layout.addWidget(self.language_combo)
        self.language_layout.addWidget(self.languages_label)
        
        # OK & Cancel buttons
        self.buttons_layout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.cancel.setDefault(True)
        self.ok = QPushButton("OK")
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.cancel)
        self.buttons_layout.addWidget(self.ok)
        
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.settings_state)
        self.layout.addLayout(self.history_layout) # à mettre dans une condition : si settings_state == True
        self.layout.addLayout(self.language_layout)
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)
        self.show()
        
    def retranslateUI(self):
        self.setWindowTitle(_("SettingsWindow","Settings"))
        self.title.setText(_("SettingsWindow","Settings"))
        self.history_label.setText(_("SettingsWindow","Maximum number of lines of your history"))
        languages = (_("SettingsWindow","English"),_("SettingsWindow","French"),_("SettingsWindow","Latin"),)
        for lang in languages:
            self.language_combo.addItem(lang)
        self.languages_label.setText(_("SettingsWindow","Choose your default language"))
        self.cancel.setText(_("SettingsWindow","Cancel"))
        self.ok.setText(_("SettingsWindow","OK"))
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
