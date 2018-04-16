#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""This file contains the classes used to print
the martyrology on the screen"""

import datetime
import martyrology as martyrology_module
import PyQt5.QtCore as QC
import PyQt5.QtWidgets as QW
import translation

_ = QC.QCoreApplication.translate



class DisplayMartyrology(QW.QTextEdit,translation.SuperTranslator):
    """Class that displays the roman martyrology"""
    martyrology = martyrology_module.Martyrology()

    def __init__(self,parent):
        QW.QTextEdit.__init__(self)
        self.parent = parent # main window
        self.initUI()

    def __call__(self,start: datetime.date,end=None,kw=None,max_result=5,rate=80):
        """Function called to display martyrology
        start must be an int if used with kw.
        Lang is found in locale
        if kw is not None, it is a list of keywords
        max_result and rate are used only with keywords"""
        if kw is not None:
            text, title = self._kw_search(kw,start,max_result,rate)
        else:
            text, title = self._date_search(start,end)

        # setting display
        self.setHtml(text)
        self.parent.setWindowTitle(title)
        self.parent.setCentralWidget(self)

    def _kw_search(self,kw: list, year: int, max_result: int, rate: 80) -> tuple:
        """Handles the keyword research.
        max_result determines the max number of texts returned.
        rate determines the minimum matching rate.
        return the text and the title to set"""
        lang = self.locale().bcp47Name()
        rate = rate/100
        results = self.martyrology.kw(kw,lang,max_nb_returned=max_result,min_ratio=rate,year=year)
        title = " ".join(kw)
        text = ""
        for elt in results:
            text += self._format_text(elt,highlight=True)
        return text, title
        

    def _date_search(self,start: datetime.date,end=None) -> tuple:
        """Function that set the text with a date research.
        return the text and the title to set."""
        lang = self.locale().bcp47Name()
        if end is None:
            title = self._title + str(start)
            end = start
        else:
            title = self._title + str(start) + ' -> ' + str(end)

        text = '' # text which will be displayed

        while start <= end:
            daytext = self.martyrology.daytext(start,lang)
            text += self._format_text(daytext)
            start += datetime.timedelta(1)

        return text, title


    def _format_text(self,daytext: martyrology_module.TextResult,highlight=False) -> str:
        """Format text, which is an entry of the
        roman martyrology for a specific day.
        highlight can be set to highlight daytext.matching_line"""
        double_nline = "<br><br>"
        black_line = "<hr />"
        paragraph = '<p>{}</p>'
        text = ""

        text += "<h1>{}</h1>".format(daytext.title)
        for i,line in enumerate(daytext.main):
            if i == daytext.matching_line:
                line = "<b>{}</b>".format(line)
            text += paragraph.format(line)
        text += paragraph.format(daytext.last_sentence)

        text += black_line
        return text



    def initUI(self):
        """Launch user interface"""
        self.setReadOnly(True)

    def retranslateUI(self):
        """Retranslate UI"""
        self._title = _("DisplayMartyrology","Theochrone - Roman Martyrology - ")

