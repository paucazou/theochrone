#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import PyQt5.QtCore as pc
import PyQt5.QtGui as pg
import PyQt5.QtWidgets as pw
from translation import *

_ = QC.QCoreApplication.translate

class SelectWindow(pw.QDialog,SuperTranslator):
    """Window to select items"""
    def __init__(self,parent):
        self.parent=parent
        pw.QWidget.__init__(self)
        SuperTranslator.__init__(self)


    def __call__(self, liste, autoselect=2):
        """liste is an iterable,
        tuple or list like
        autoselect indicates the number of items
        that must be selected and greyed"""
        self.autoselect = autoselect
        self.items = liste
        self.items_checkboxes = []
        self.results = []

        self.initUI()
        self.retranslateUI()

    def initUI(self):
        """Initializes the window
        """
        # message
        message_font = pg.QFont()
        message_font.setPointSize(15)
        self.message = pw.QLabel('Select the items you want to export')
        self.message.setFont(message_font)
        self.message.setAlignment(pc.Qt.AlignHCenter)

        # items
        ## items layout
        self.core_layout = pw.QHBoxLayout()
        self.left_column = pw.QVBoxLayout()
        self.right_column = pw.QVBoxLayout()
        self.core_layout.addLayout(self.left_column)
        self.core_layout.addLayout(self.right_column)

        ## dispatching items
        for i, elt in enumerate(self.items):
            layout = self.left_column if i % 2 == 0 else self.right_column
            self.items_checkboxes.append(pw.QCheckBox(elt,self))
            layout.addWidget(self.items_checkboxes[-1])
            if i < self.autoselect: #name and date
                self.items_checkboxes[-1].setChecked(True)
                self.items_checkboxes[-1].setDisabled(True)

        # OK & Cancel buttons
        self.buttons_layout = pw.QHBoxLayout()
        self.cancel = pw.QPushButton("Cancel")
        self.ok = pw.QPushButton("Ok")
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.cancel)
        self.buttons_layout.addWidget(self.ok)
        ## logic
        self.ok.clicked.connect(self.setResults)
        self.cancel.clicked.connect(self.close)


        # main layout
        self.layout = pw.QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addLayout(self.core_layout)
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

        #geometry
        self.move(self.parent.geometry().topLeft())
        self.exec()

    def retranslateUI(self):
        """Retranslate the whole window if necessary"""
        self.setWindowTitle(_("SelectWindow","Select items"))
        self.message.setText(_("SelectWindow","Select the items you want to export"))
        self.ok.setText(_("SelectWindow","OK"))
        self.cancel.setText(_("SelectWindow","Cancel"))

    def setResults(self):
        """Called by a click to OK"""
        self.results = [elt.isChecked() for elt in self.items_checkboxes]
        self.close()
