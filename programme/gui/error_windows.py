#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import os
import sys

chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/..')
sys.path.append(programme)
sys.path.append(chemin)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox
from translation import *

_ = QCoreApplication.translate

class ErrorWindow(QMessageBox,SuperTranslator):
    """Window for errors"""

    def __init__(self,message,title=_("ErrorWindow","Error"),icon=QMessageBox.Warning):
        QMessageBox.__init__(self)
        SuperTranslator.__init__(self)
        self.message = message
        self.title = title
        self.Icon = icon
        self.initUI()

    def initUI(self):
        self.setIcon(self.Icon)
        self.setWindowTitle(self.title)
        self.setText(self.message)
        self.exec()

    def retranslateUI(self):
        pass

