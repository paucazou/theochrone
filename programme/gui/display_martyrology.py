#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""This file contains the classes used to print
the martyrology on the screen"""

import datetime
import martyrology
import PyQt5.QtCore as QC
import PyQt5.QtWidgets as QW
import translation

_ = QC.QCoreApplication.translate


#TODO : FROM CLI AND PRINTER

class DisplayMartyrology(QW.QTextEdit,translation.SuperTranslator):
    """Class that displays the roman martyrology"""
    martyrology = martyrology.Martyrology()

    def __init__(self,parent):
        QW.QTextEdit.__init__(self)
        self.parent = parent # main window
        self.initUI()

    def __call__(self,start: datetime.date,end=None,kw=None):
        """Function called to display martyrology
        Lang is found in locale"""
        lang = self.locale().bcp47Name()
        if end is None:
            title = self._title + str(start)
            end = start
        else:
            title = self._title + str(start) + ' -> ' + str(end)

        text = '' # text which will be displayed
        double_nline = "<br><br>"
        line = "<hr />"

        while start <= end:
            daytext = self.martyrology.daytext(start,lang)
            text += "<h1>{}</h1>".format(daytext.title)
            text += double_nline.join(daytext.main) + double_nline + daytext.last_sentence
            text += line
            start += datetime.timedelta(1)

        # setting display
        self.setHtml(text)
        self.parent.setWindowTitle(title)
        self.parent.setCentralWidget(self)


    def initUI(self):
        """Launch user interface"""
        self.setReadOnly(True)

    def retranslateUI(self):
        """Retranslate UI"""
        self._title = _("DisplayMartyrology","Theochrone - Roman Martyrology - ")

