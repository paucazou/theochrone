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

import qml
import images

class App(QApplication):
    def __init__(self, args):
        app = QApplication(args)
        engine = QQmlApplicationEngine()
        engine.quit.connect(app.quit)
        engine.load(chemin + "/qml/main.qml")
        sys.exit(app.exec_())