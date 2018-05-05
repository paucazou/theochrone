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
    def __init__(self,parent):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.parent = parent
        
        self.languages = ('en','fr')#,'la')
        self.initUI()
        self.retranslateUI()
    
    def initUI(self):
        #title
        title_font = QFont()
        title_font.setPointSize(20)
        self.title = QLabel('Settings')
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignHCenter)
            
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

        # proper choice
        self.propers_layout = QHBoxLayout()
        self.propers_combo = QComboBox()
        self.propers_label = QLabel("Choose your preferred proper")
        self.propers_layout.addWidget(self.propers_combo)
        self.propers_layout.addWidget(self.propers_label)
        
        # OK & Cancel buttons
        self.buttons_layout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.cancel.setDefault(True)
        self.ok = QPushButton("OK")
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.cancel)
        self.buttons_layout.addWidget(self.ok)
        
        # Main checkbox
        self.settings_state = QCheckBox('Set settings off',self)
        self.settings_state.toggle()
        self.settings_state.stateChanged.connect(self.SettingState)
        if not officia.pdata():
            self.settings_state.setChecked(False)
        else:
            self.settings_state.setChecked(True)
            
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.settings_state)
        self.layout.addLayout(self.history_layout)
        self.layout.addLayout(self.language_layout)
        self.layout.addLayout(self.propers_layout)
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)
        
        # Buttons
        self.ok.clicked.connect(self.saveSettings)
        self.cancel.clicked.connect(self.close)
        
        # geometry
        self.move(self.parent.geometry().topLeft())
        self.show()
        
    def retranslateUI(self):
        self.setWindowTitle(_("SettingsWindow","Settings"))
        self.title.setText(_("SettingsWindow","Settings"))
        self.history_label.setText(_("SettingsWindow","Maximum number of lines of your history"))
        # lang
        languages = (_("SettingsWindow","English"),_("SettingsWindow","French"))#,_("SettingsWindow","Latin"),)
        self.language_combo.clear()
        for lang in languages:
            self.language_combo.addItem(lang)
        lang = officia.pdata(language_saved=True)
        if lang:
            index = self.languages.index(lang)
        else:
            index = 0
        self.language_combo.setCurrentIndex(index)

        # proper
        for proper in self.parent.propers:
            self.propers_combo.addItem(proper[1])
        proper = officia.pdata(proper_saved=True)
        if proper:
            self.propers_combo.setCurrentText(self.parent.propersDict[proper])

        self.languages_label.setText(_("SettingsWindow","Choose your default language"))
        self.propers_label.setText(_('SettingsWindow',"Choose your default proper"))
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
        
    def saveSettings(self):
        # TODO save proper
        proper_id = self.propers_combo.currentIndex()
        proper_name = self.parent.propers[proper_id][0]
        officia.pdata(langue=str(self.languages[self.language_combo.currentIndex()]),
                      max_history=str(self.history_lines.value()),
                      proper=proper_name,
                      )
        self.close()
