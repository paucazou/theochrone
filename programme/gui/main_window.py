#!/usr/bin/python3
# -*-coding:Utf-8 -*
# Deus in adjutorium meum intende

import calendar
import datetime
import os.path
import platform
import sys
import webbrowser
import xlwt

chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/..')
sys.path.append(programme)
sys.path.append(chemin)
import adjutoria
import annus
import collections
import error_windows
import exporter
import display_martyrology 
import math
import officia
import settings
os.chdir(chemin)

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QCoreApplication, QDate, QLineF, QLocale, QPoint, QRect, QRectF, QSize, Qt, QTranslator
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QIcon, QPen, QPainter, QTextDocument
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import QAbstractItemView, QAction, QApplication, QButtonGroup, QCalendarWidget, QCheckBox, QComboBox, QDateEdit, QDockWidget, QFileDialog, QGroupBox, QHBoxLayout, QMainWindow, QLabel, QLineEdit, QPushButton, QSizePolicy, QSlider, QSpinBox, QStyle, QTableWidget, QTableWidgetItem, QTabWidget, QToolBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from state import State
from translation import *


_ = QCoreApplication.translate # a name more convenient
current = QDate().currentDate()
calendrier = calendar.Calendar(firstweekday=6)
first_upper = lambda x : x[0].upper() + x[1:]
list_depth = lambda L: isinstance(L, list) and max(map(depth, L),default=0)+1 #http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to 
dic_depth = lambda d, depth=0: isinstance(d,dict) and max(dic_depth(v, depth+1) for k, v in d.items()) +1 #https://stackoverflow.com/questions/9538875/recursive-depth-of-python-dictionary
            
class YearSpinbox(QSpinBox):
    """A class which defines a spinbox widget specifically to display a set of years from 1600 to 4100."""
    def __init__(self):
        QSpinBox.__init__(self)
        self.setMinimum(1600)
        self.setMaximum(4100)
        self.setValue(current.year())
            
class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)
        self.translator = QTranslator()
        self.installTranslator(self.translator)
        self.execute = Main(self,args)


class Main(QMainWindow,SuperTranslator):
    """Main window"""
    def __init__(self,parent,args):
        """Function which initializes the main window"""
        
        QMainWindow.__init__(self)
        SuperTranslator.__init__(self)

        self.parent = parent

        self.__calendars = {}
        self.state = State(self) # state of the central widget
        self.ferryman = ExportResults(self)
        self.actions()
        self.initUI()
        
        self.W.onglets.W.tab1.cal.clicked.connect(self.useDate)
        self.W.onglets.W.tab1.kw_bouton.clicked.connect(self.useKeyWord)
        self.W.onglets.W.tab1.keyword.returnPressed.connect(self.useKeyWord)
        #self.W.onglets.W.tab1.spinbox.editingFinished.connect(self.useKeyWord)
        
        self.W.onglets.W.tabPlus.bt_week.clicked.connect(self.useWeek)
        #self.W.onglets.W.tabPlus.wy_spinbox.editingFinished.connect(self.useWeek)
        
        self.W.onglets.W.tabPlus.bt_month.clicked.connect(self.useMonth)
        #self.W.onglets.W.tabPlus.my_spinbox.editingFinished.connect(self.useMonth)
        
        #self.W.onglets.W.tabPlus.yy_spinbox.editingFinished.connect(self.useYear)
        self.W.onglets.W.tabPlus.bt_year.clicked.connect(self.useYear)
        
        self.W.onglets.W.tabPlus.bt_arbitrary.clicked.connect(self.useArbitrary)
        #self.W.onglets.W.tabPlus.to.editingFinished.connect(self.useArbitrary)
        #self.W.onglets.W.tabPlus.frome.editingFinished.connect(self.useArbitrary)

        self.processCommandLineArgs(args)
        
    def processCommandLineArgs(self,args): 
        # TODO if we got enough time, try to detect week, month and year and use matching boxes
        args, debut, fin = args
        reverse, plus = args.INVERSE, args.plus
        self.pal.setChecked(args.pal)

        if args.martyrology:
            self.martyrology_box.setChecked(args.martyrology) 
            self.W.mainToolbar.martyrologyCheckedActions()
        self.W.mainToolbar.selectProper.setCurrentText(self.propersDict[args.propre])
        if reverse != 1:
            self.W.onglets.W.tab1.keyword.setText(' '.join(reverse))
            self.W.onglets.W.tab1.spinbox.setValue(debut.year)
            if plus:
                self.W.onglets.W.tab1.plus.setChecked(True)
            self.useKeyWord()
        elif debut == fin:
            self.W.onglets.W.tab1.cal.setSelectedDate(QDate(debut))
            self.useDate()
        elif debut != fin:
            frome = self.W.onglets.W.tabPlus.frome
            while frome.date().toPyDate() != debut:
                frome.setDate(QDate(debut.year,debut.month,debut.day))
                self.W.onglets.W.tabPlus.to.setDate(QDate(fin.year,fin.month,fin.day))
            self.useArbitrary()
            self.W.onglets.tabs.setCurrentIndex(1)

        if args.langue == 'fr':
            self.setLocaleFr()
        else:
            self.setLocaleEn()
        
    def menu(self):
        """A function which describes the menubar of the main window"""
        menubar = self.menuBar()
        if sys.platform.startswith('darwin') or '32bit' in platform.architecture(): # TODO make a special class for each platform ?
            menubar.setNativeMenuBar(False)
        
        # File menu
        self.fileMenu = menubar.addMenu('file')
        self.fileMenu.addAction(self.settingsAction)
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.exportPDF)
        self.fileMenu.addAction(self.exportSpreadsheet)
        self.fileMenu.addAction(self.exportIcs)
        self.fileMenu.addAction(self.exitAction)
        
        # Edit menu
        #self.editMenu = menubar.addMenu('edit')
        
        # Language menu (change on the fly)
        self.languageMenu = menubar.addMenu('language')
        #self.languageMenu.addAction(self.chooseLanguageLatin)
        self.languageMenu.addAction(self.chooseLanguageFrench)
        self.languageMenu.addAction(self.chooseLanguageEnglish)
        
        # Help menu
        #self.helpMenu = menubar.addMenu('help')
        
    def actions(self): # WARNING not available on os x
        """A function which defines actions in the main window"""
        ctrl = 'Ctrl+'
        
        #File
        # Settings
        self.settingsAction = QAction(QIcon('icons/settings.png'),'settings',self) # icons https://www.iconfinder.com/icons/353407/cog_settings_icon#size=128
        self.settingsAction.triggered.connect(self.openSettings)
        self.settingsAction.setShortcut(ctrl+'S')
        # Print
        self.printAction = QAction(QIcon('icons/print.png'),'print',self) # https://www.iconfinder.com/icons/392497/print_printer_printing_icon#size=128
        self.printAction.setShortcut(ctrl+'P')
        self.printAction.triggered.connect(self.ferryman.exportToPrinter)
        # PDF
        self.exportPDF = QAction(QIcon('icons/pdf.png'),'export as PDF',self) # https://www.iconfinder.com/icons/83290/file_pdf_icon#size=32
        self.exportPDF.triggered.connect(self.ferryman.exportAsPDF)
        self.exportPDF.setShortcut(ctrl+'D')
        # Excel
        self.exportSpreadsheet = QAction(QIcon('icons/spreadsheet.svg'),'Export to spreadsheet',self)
        self.exportSpreadsheet.triggered.connect(self.ferryman.exportToSpreadsheet)
        self.exportSpreadsheet.setShortcut(ctrl+'X')
        # ICS
        self.exportIcs = QAction(QIcon('icons/ics.svg'),'Export as ICS calendar',self)
        self.exportIcs.triggered.connect(self.ferryman.exportToIcs)
        self.exportIcs.setShortcut(ctrl+'I')
        # Exit
        self.exitAction = QAction(QIcon('icons/exit.png'),'exit_name',self)
        self.exitAction.setShortcut(ctrl+'Q')
        self.exitAction.triggered.connect(self.close)
        
        # Languages
        ## Latin
        #self.chooseLanguageLatin = QAction(QIcon('icons/latin.png'),'choose_latin',self) # à lier dans la classe App pour changer de langue
        ## French
        self.chooseLanguageFrench = QAction(QIcon('icons/french.png'),'choose_french',self)
        self.chooseLanguageFrench.triggered.connect(self.setLocaleFr)
        ## English
        self.chooseLanguageEnglish = QAction(QIcon('icons/english.png'),'choose_english',self)
        self.chooseLanguageEnglish.triggered.connect(self.setLocaleEn)


                                           
        
    def initUI(self):
        """A function which defines widgets and main features of the window"""
        
        # widgets
        # main widget
        self.arbre = QTreeWidget() # TODO seems to be useless...
        # widgets on the right
        self.rightDock = QDockWidget('right_dock',self)
        self.rightDock.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
        self.W.onglets = Onglets(self)
        self.rightDock.setWidget(self.W.onglets)
        self.addDockWidget(Qt.RightDockWidgetArea,self.rightDock)
        
        # menu
        self.menu()        
        
        # statusbar
        self.statusBar()

        # toolbar
        self.W.mainToolbar = ToolBar(self)
        self.addToolBar(self.W.mainToolbar)
        self.pal = self.W.mainToolbar.pal
        self.martyrology_box = self.W.mainToolbar.martyrology_box

        #Roman Martyrology
        self.W.martyrology = display_martyrology.DisplayMartyrology(self)
        
        # main features
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight,Qt.AlignCenter,self.size(),App.desktop().availableGeometry()))
        self.retranslateUI() # voir si on ne la met pas carrément dans l'app, qui hériterait elle aussi de SuperTranslator
        # default settings
        self.W.onglets.W.tabPlus.month_combo.setCurrentIndex(current.month() - 1)
        self.W.onglets.W.tabPlus.monthweek_combo.setCurrentIndex(current.month() - 1)
        self.W.onglets.W.tabPlus.change_weeks()
        self.show()
        
    def retranslateUI(self):
        
        #menu
        self.fileMenu.setTitle(_('Main','File'))
        #self.editMenu.setTitle(_('Main','Edit'))
        self.languageMenu.setTitle(_('Main','Language'))
        #self.helpMenu.setTitle(_('Main','Help'))
        
        #actions
        self.settingsAction.setText(_('Main','Settings'))
        
        self.printAction.setText(_('Main','Print'))
        self.exportPDF.setText(_('Main','Export as PDF'))
        self.exportSpreadsheet.setText(_('Main','Export as spreadsheet'))
        self.exportIcs.setText(_('Main','Export as ICS calendar'))
        
        self.exitAction.setText(_('Main','Exit'))
        self.exitAction.setStatusTip(_('Main','Exit the app'))
        
        #self.chooseLanguageLatin.setText(_('Main','Latin'))
        self.chooseLanguageFrench.setText(_('Main','French'))
        self.chooseLanguageEnglish.setText(_('Main','English'))

        # propers
        self.propers = [
                ('roman'         ,_('Toolbar','Roman')),
                ('australian'    ,_('Toolbar','Australian')),
                ('american'      ,_('Toolbar','American')),
                ('brazilian'     ,_('Toolbar','Brazilian')),
                ('canadian'      ,_('Toolbar','Canadian')),
                ('english'       ,_('Toolbar','English')),
                ('french'        ,_('Toolbar','French')),
                ('newzealander' ,_('Toolbar','New-Zealander')),
                ('polish'        ,_('Toolbar','Polish')),
                ('portuguese'    ,_('Toolbar','Portuguese')),
                ('scottish'      ,_('Toolbar','Scottish')),
                ('spanish'       ,_('Toolbar','Spanish')),
                ('welsh'         ,_('Toolbar','Welsh'),),
                ]
        self.propersDict = collections.OrderedDict(self.propers) # a convenient way to access to names of propers

        SuperTranslator.retranslateUI(self) # must be called at the end, because some data must be shared with children

        
        #initUI
        #widgets on the right
        self.rightDock.setWindowTitle(_('Main','Research'))
        
    def _selectLanguage(self,loc=SuperTranslator.enLocale):
        """Select another language for the app."""
        self.setLocale(loc)
        self.lang = self.locale().bcp47Name()
        self.parent.translator.load(loc,"theochrone",'.',chemin + '/i18n/','.qm') 
        #TODO reload translation of core app
        #while True: # this horrible loop tries to avoid the RuntimeError:wrapped C/C++ object of type Table has been deleted
        try:
            self.retranslateUI()
            #break
        except RuntimeError:
            pass
        
        self.state.reload()
    
    def setLocaleFr(self):
        """Set fr as main language"""
        self._selectLanguage(self.frLocale)

    def setLocaleEn(self):
        """Set en as main language"""
        self._selectLanguage(self.enLocale)

    def openSettings(self): # passer un argument concernant la langue choisie
        self.W.settings = settings.SettingsWindow(parent=self)

    def getCalendar(self,proper='roman',ordo=1962) -> annus.LiturgicalCalendar:
        """Get a liturgical calendar with requested values.
        The calendar may or not be already set"""
        if proper not in self.__calendars:
            self.__calendars[proper] = annus.LiturgicalCalendar(proper=proper,ordo=ordo)
        return self.__calendars[proper]

    def getCalendarLoaded(self,start: int, end=None) -> annus.LiturgicalCalendar:
        """Wrapper of getCalendar. Loads years requested (start,end).
        proper is selected thanks to the QComboBox selectProper
        """
        proper_id = self.W.mainToolbar.selectProper.currentIndex()
        proper = self.propers[proper_id][0] # zero match with the name of the proper
        lcalendar = self.getCalendar(proper)
        if end is None:
            end = start
        lcalendar(start,end)
        return lcalendar

    def setCentralWidget(self,widget,**kwargs):
        """Set the central widget.
        Pass kwargs to the state object.
        Modifies things linked to the change
        of this state"""
        QMainWindow.setCentralWidget(self,widget)
        self.state(**kwargs)

        on = (self.state.type == "martyrology") # on is a bool which is set many times
        self.exportSpreadsheet.setEnabled(not on)

        on = (self.state.type in ("kw","martyrology"))
        self.exportIcs.setEnabled(not on)

        
    def useDate(self):
        date = self.W.onglets.W.tab1.cal.selectedDate()
        debut = fin = date.toPyDate()
        span = "day"
        if self.martyrology_box.isChecked():
            self.W.martyrology(debut,span=span)
        else:
            self.setWindowTitle('Theochrone - ' + self.localizedDate(day=debut))
            lcalendar = self.getCalendarLoaded(start=debut.year)
            selection = lcalendar[debut]
            pal = self.pal.isChecked()
            self.tableau = Table(self,selection,lcalendar,pal=pal)
            self.setCentralWidget(self.tableau,type="date",span=span,data=selection,pal=pal)
            officia.pdata(write=True,history='dates',debut=debut,fin=fin)
        
    def useKeyWord(self):

        keyword = self.W.onglets.W.tab1.keyword.text()
        annee = self.W.onglets.W.tab1.spinbox.value()
        if keyword == '':
            return

        if self.martyrology_box.isChecked():
            keyword = keyword.split()
            max_result = self.W.onglets.W.tab1.max_result.value()
            rate = self.W.onglets.W.tab1.rate_result.value()
            self.W.martyrology(annee,kw=keyword,max_result=max_result,rate=rate)
        else:
            if False and self.lang == 'en': ## TODO TODO
                return error_windows.ErrorWindow("Keyword research is not yet available in english.\n Can you give us some help?")
            self.setWindowTitle('Theochrone - ' + keyword)
            debut, fin = datetime.date(annee,1,1), datetime.date(annee, 12,31)
            lcalendar = self.getCalendarLoaded(debut.year)
            if self.W.onglets.W.tab1.plus.isChecked():
                plus = True
            else:
                plus = False
            selection = officia.inversons(keyword,lcalendar,debut,fin,exit=False,plus=plus,langue=self.lang) 
            if isinstance(selection[0],str):#BUG : list index out of range. research: 2018, spanish, patron
                return error_windows.ErrorWindow(selection[0])
            self.W.tableau = Table(self,selection,lcalendar,inverse=True,pal=self.pal.isChecked())
            self.setCentralWidget(self.W.tableau,type="kw",year=annee,data=selection)
            officia.pdata(write=True,history='reverse',debut=debut,fin=fin,keywords=[keyword])
            
    def useWeek(self):
        span = "week"
        tab=self.W.onglets.W.tabPlus
        year = tab.wy_spinbox.value()
        month = tab.monthweek_combo.currentIndex() + 1
        week = tab.week_combo.currentIndex()
        lcalendar = self.getCalendarLoaded(year)
        WEEK = lcalendar.weekmonth(year,month,week)
        week_dates = sorted(WEEK.keys())
        start, end = week_dates[0],week_dates[-1]
        if self.martyrology_box.isChecked():
            self.W.martyrology(start,end,span=span)
        else:
            self.W.arbre = Tree(self,WEEK,lcalendar,self.pal.isChecked())
            self.setCentralWidget(self.W.arbre,type="date",span=span,data=WEEK,weeknb=week,pal=self.pal.isChecked())
            self.setWindowTitle('Theochrone - {}'.format(self.localizedDate(
                week=week+1,month=month,year=year)))
            debut, fin = sorted(WEEK)[0], sorted(WEEK)[-1]
            officia.pdata(write=True,history='dates',debut=debut,fin=fin,semaine_seule=True)
            
    def useMonth(self):
        span = "month"
        tab = self.W.onglets.W.tabPlus
        year = tab.my_spinbox.value()
        month = tab.month_combo.currentIndex() + 1
        start = datetime.date(year,month,1)
        end = datetime.date(year,month,calendar.monthrange(year,month)[-1])
        if self.martyrology_box.isChecked():
            self.W.martyrology(start,end,span=span)
        else:
            lcalendar = self.getCalendarLoaded(year)
            MONTH = lcalendar.listed_month(year, month)
            self.W.arbre = Tree(self,MONTH,lcalendar,self.pal.isChecked())
            self.setCentralWidget(self.W.arbre,type="date",span=span,data=MONTH,pal=self.pal.isChecked())
            self.setWindowTitle('Theochrone - {}'.format(
                self.localizedDate(month=month,year=year)))
            #debut = next(iter(sorted(next(iter(MONTH.values()))))) # Do you know this is horrible and useless ?
            debut = datetime.date(year,month,1)
            fin_day = calendar.monthrange(year,month)[1]
            fin = datetime.date(year,month,fin_day)
            officia.pdata(write=True,history='dates',debut=debut,fin=fin,mois_seul=True)
        
    def useYear(self):
        span="year"
        tab = self.W.onglets.W.tabPlus
        year = tab.yy_spinbox.value()
        start = datetime.date(year,1,1)
        end = datetime.date(year,12,31)
        if self.martyrology_box.isChecked():
            self.W.martyrology(start,end,span=span)
        else:
            lcalendar = self.getCalendarLoaded(year)
            YEAR = lcalendar.listed_year(year)
            self.W.arbre = Tree(self,YEAR,lcalendar,self.pal.isChecked())
            self.setCentralWidget(self.W.arbre,type="date",span=span,data=YEAR,pal=self.pal.isChecked())
            self.setWindowTitle('Theochrone - {}'.format(str(year)))
            officia.pdata(write=True,history='dates',debut=datetime.date(year,1,1),fin=datetime.date(year,12,31),annee_seule=True)
        
    def useArbitrary(self):
        span="arbitrary"
        tab = self.W.onglets.W.tabPlus
        debut = tab.frome.date().toPyDate()
        fin = tab.to.date().toPyDate()
        if self.martyrology_box.isChecked():
            self.W.martyrology(debut,fin,span=span)
        else:
            lcalendar = self.getCalendarLoaded(debut.year,fin.year)
            RANGE = lcalendar.listed_arbitrary(debut,fin)
            self.W.arbre = Tree(self,RANGE,lcalendar,self.pal.isChecked())
            self.setCentralWidget(self.W.arbre,type="date",start=debut,end=fin,span=span,data=RANGE,pal=self.pal.isChecked(),proper=lcalendar.proper,ordo=lcalendar.ordo)
            self.setWindowTitle('Theochrone - {} -> {}'.format(
                self.localizedDate(day=debut),
                self.localizedDate(day=fin)))
            officia.pdata(write=True,history='dates',debut=debut,fin=fin,fromto=True)
        

class ToolBar(QToolBar,SuperTranslator):
    """This class manages the toolbar"""
    def __init__(self,parent):
        """Inits the toolbar"""
        QToolBar.__init__(self)
        SuperTranslator.__init__(self)

        self.parent = parent # main window
        self.initUI()

    def initUI(self):
        """Fill the toolbar"""
        # set a spacer in order to right align some widgets, if useful
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        ## actions in Toolbar
        self.nextButtonAction = QAction(QIcon('icons/next.png'),'next',self) #https://www.iconfinder.com/icons/308956/arrow_next_icon#size=256
        self.previousButtonAction = QAction(QIcon('icons/previous.png'),'previous',self) #https://www.iconfinder.com/icons/308957/arrow_previous_icon#size=256
        # TODO add a reload button ? 

        ## widgets in Toolbar
        self.selectProper = QComboBox() # fill it with propers available

        self.pal = QCheckBox('Include Pro Aliquibus Locis')
        self.martyrology_box = QCheckBox('Search in Roman Martyrology')
       
        ## set actions in Toolbar
        self.addAction(self.previousButtonAction)
        self.addAction(self.nextButtonAction)

        self.addWidget(self.selectProper)
        self.addWidget(self.pal)
        self.addWidget(self.martyrology_box) 

        self.connect()


    def connect(self):
        """Connect widgets between them"""
        self.pal.clicked.connect(self.setUncheckedMartyrology)
        self.martyrology_box.clicked.connect(self.martyrologyCheckedActions)
        self.nextButtonAction.triggered.connect(self.parent.state.next)
        self.previousButtonAction.triggered.connect(self.parent.state.previous)

    def setUncheckedMartyrology(self):
        """Wrapper. Uncheck the martyrology checkbox"""
        if self.pal.isChecked():
            self.martyrology_box.setChecked(False)
            self.martyrologyCheckedActions()
            self.pal.setChecked(True) # a bit silly... but self.martyrologyCheckedActions set unchecked just before...

    def martyrologyCheckedActions(self):
        """When toggled on, martyrology set or unset
        following things:
        - desactivate pro aliquibus locis
        - des/activate plus button in keyword research
        - des/activate a slidebar in kw research
        - des/activate a spinbox in kw research
        - set inactive the export to spreadsheet entry in file menu
        """
        one_tab = self.parent.W.onglets.W.tab1
        on = True if self.martyrology_box.isChecked() else False # why this condition ? -> better -> on = self.martyrology_box.isChecked()

        self.pal.setChecked(False) 
        one_tab.plus.setVisible(not on)
        one_tab.max_result.setVisible(on)
        one_tab.rate_result.setVisible(on)
        one_tab.rate_result_label.setVisible(on)
        one_tab.max_result_label.setVisible(on)


            
            


    def retranslateUI(self):
        """Retranslate the toolbar"""
        ##actions
        self.nextButtonAction.setText(_('Main','Next'))
        self.previousButtonAction.setText(_('Main','Previous'))
        ##widgets
        self.pal.setText(_('Toolbar','Include Pro Aliquibus Locis'))
        self.martyrology_box.setText(_('ToolBar','Search in Roman Martyrology'))
        # propers
        self.selectProper.clear()
        for proper in self.parent.propers:
            self.selectProper.addItem(proper[1])
        
class ExportResults(SuperTranslator):
    """Manage the exports in other formats.
    For now : PDF, print"""
    
    def __init__(self,parent):
        SuperTranslator.__init__(self)
        self.parent = parent
        self.printer = QPrinter(QPrinter.HighResolution)
        self.painter = QPainter()
        self.currentPoint = QPoint(0,0)
        self.printDialog = QPrintDialog(self.printer,self.parent)
        self.printDialog.setWindowTitle(_('ExportResults','Print results'))
        self.personal_directory = os.path.expanduser('~')
        self.retranslateUI()
        
    def extractTreeData(self,parent=None):
        """Returns the data as they appeared on the screen"""
        data = collections.OrderedDict()
        liste = []
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.columnCount() == 1:
                data[child.text(0)] = self.extractTreeData(parent=child)
            else:
                liste.append([child.text(j) for j in range(child.columnCount()) if child.text(j)])
        if not liste:
            return data
        else:
            return liste
    
    def formatTreeData(self,data,ndata,title=''):
        for key,value in data.items():
            if dic_depth(value) == 0:
                ndata[title[:-3]] = data
                return ndata
            else:
                self.formatTreeData(value,ndata,title + key + " : ")
        return ndata
        
            
    def extractData(self):
        if isinstance(self.parent.centralWidget(),Tree):
            header_item = self.parent.centralWidget().headerItem()
            headers = [ header_item.text(i) for i in range(header_item.columnCount()) ]
            data = self.extractTreeData(self.parent.centralWidget().invisibleRootItem())
            if dic_depth(data) != 1:
                data = self.formatTreeData(data,collections.OrderedDict())
        else:
            table = self.parent.centralWidget()
            headers = [ table.horizontalHeaderItem(i).text() for i in range(table.columnCount()) ]
            nb_lines = table.rowCount()
            item = table.item
            data = {item(i,0).text():[] for i in range(nb_lines) if item(i,0) }
            for row in range(nb_lines):
                data[item(row,0).text()].append(
                    [item(row,i).text() for i in range(1,table.columnCount()) if item(row,i).text()]
                     )        
        return headers, data

    def exportToIcs(self):
        """Export data to the ICS format, useful
        for Outlook/Google/Thunderbird calendars."""
        dialog = QFileDialog.getSaveFileName(self.parent,self.exportAsIcsTitle,self.personal_directory,self.typeIcsFiles)
        if dialog[0]:
            file = open(dialog[0],'w')
            state = self.parent.state

            exporter.main(state.start,state.end, # dates
                    self.parent.locale().bcp47Name(), # lang
                    file,
                    proper=state.proper,ordo=state.ordo,
                    file_ext="ics",
                    pal=state.pal) # options
            file.close()


        
    def exportToSpreadsheet(self):# TODO mettre les cases à la bonne taille, changer les dates en dates Excel
        """Export current data to spreadsheet"""
        headers, data = self.extractData()
        book = xlwt.Workbook()
        sheet = book.add_sheet(self.parent.windowTitle())
        for i, elt in enumerate(headers):
            sheet.write(0,i,elt)
        row = 1
        self.spreadsheetlist = []
        self.iterSpreadsheet(data)
        for elt in self.spreadsheetlist:
            [sheet.write(row,i,text) for i, text in enumerate(elt)]
            row += 1
        dialog = QFileDialog.getSaveFileName(self.parent,self.exportAsSheetTitle,self.personal_directory,self.typeSheetFiles)
        if dialog[0]:
            book.save(dialog[0])
    
    def iterSpreadsheet(self,raw_data):
        """Recursive function which append data to self.spreadsheetlist"""
        for key, value in raw_data.items():
            if isinstance(value,list):
                [self.spreadsheetlist.append([key] + elt) for elt in value]
            else:
                self.iterSpreadsheet(value)
    
    def defineLook(self):
        """Method which will be filled by a dialog window"""
        self.font = 'Arial'
        
    def exportToPrinter(self):
        preview = QPrintPreviewDialog(self.printer)
        if isinstance(self.parent.centralWidget(),display_martyrology.DisplayMartyrology):
            preview.paintRequested.connect(self.parent.centralWidget().print)
        else:
            preview.paintRequested.connect(self.paintController)
        preview.exec()
        
    def exportAsPDF(self):
        dialog = QFileDialog.getSaveFileName(self.parent,self.exportAsPdfTitle,self.personal_directory,self.typeFiles)
        if dialog[0]:
            self.printer.setOutputFormat(QPrinter.PdfFormat)
            self.printer.setOutputFileName(dialog[0])
            if isinstance(self.parent.centralWidget(),display_martyrology.DisplayMartyrology):
                self.parent.centralWidget().print(self.printer)
            else:
                self.paintController()
            
    def paintController(self):
        """Manage the main painting"""
        self.defineLook()
        paper_rect = self.printer.paperRect()
        self.printer.setFullPage(True)
        self.left = paper_rect.left() + (paper_rect.width() *5/100)
        self.top = paper_rect.top() + (paper_rect.height() *5/100)
        self.right = paper_rect.right() - (paper_rect.width() *10/100)
        self.bottom = paper_rect.bottom() - (paper_rect.height() *10/100)
        self.page_rectangle = QRect(self.left,self.top,self.right,self.bottom)
        
        self.currentPoint.setY(self.top)
        self.currentPoint.setX(self.left)
        self.preparePen(20,Qt.SolidLine,Qt.blue)
        
        self.painter.begin(self.printer)
        #self.painter.drawRect(self.page_rectangle)
        self.paintMainTitle()
        headers, data = self.extractData()
        self.iterPainter(data,headers[(isinstance(self.parent.centralWidget(),Table) + 1):])
        #self.paintIntermediateTitles('2017 : janvier : sixième semaine')
        #self.paintSubtitles('Vendredi premier janvier 2017')
        #self.paintFeasts(('Classe','Statut','Couleur'),('Vendredi de la première semaine de Carême','Deuxième classe','Célébrée','Violet'))
        self.painter.end()
        
    def iterPainter(self,data,headers):
        """Iters into data to paint correctly titles and feasts"""
        for key, value in data.items():
            if dic_depth(data) == 1:
                self.goonOrNewPage(2,len(value[0]))
                self.paintSubtitles(key)
                for item in value:
                    self.goonOrNewPage(1,len(item))
                    self.paintFeasts(headers,item)
            else:
                nb_items = len([elt for elt in value.values()][0][0])
                self.goonOrNewPage(3,nb_items)
                self.paintIntermediateTitles(key)
                self.iterPainter(value,headers)
    
    def goonOrNewPage(self,level,nb_items):
        """This method checks if there is enough place on the page.
        If not, start a new page.
        level is an int : 1 : only new feasts
        2 : a feast + a subtitle
        3 : a feast + a subtitle + an intermediate Title
        nb_items : int : number of items to print"""
        height = 0
        available_place = self.bottom - self.currentPoint.y()
        if level >= 1: # feast
            height += self.page_rectangle.height()*3/100 # name of the feast
            height += self.createHRectangles(2,3).height()*(nb_items + 1)/2 # every other item
        if level >= 2: # feast + subtitle 
            height += self.page_rectangle.height()*3/100
        if level == 3: # feast + subtitle + intermediate title
            height += self.page_rectangle.height()*4/100
        if height > available_place:
            self.printer.newPage()
            self.currentPoint.setY(self.top)
            self.currentPoint.setX(self.left)
  
    def preparePen(self,width,style,color=Qt.black):
        pen = QPen(style)
        pen.setColor(QColor(color))
        pen.setWidth(width)
        self.painter.setPen(pen)
        
    def paintMainTitle(self):
        """Paint the main title, ie the research keywords"""
        self.preparePen(20,Qt.SolidLine)
        title = self.parent.windowTitle()
        fontSize = 25
        percentage = 10
        while True:
            rectangle_title = QRect(self.page_rectangle.left(),self.page_rectangle.top(),self.page_rectangle.width(),self.page_rectangle.height()/percentage)
            fontCandidate = QFont(self.font,fontSize)
            self.painter.setFont(fontCandidate) # TODO aligner à gauche ?
            if self.painter.boundingRect(QRect(),Qt.AlignCenter,title).width() < self.page_rectangle.width():
                break
            else:
                fontSize -= 1
                percentage += 1
        self.painter.drawText(rectangle_title,Qt.AlignCenter,title)
        self.painter.drawLine(QLineF(rectangle_title.bottomLeft(),rectangle_title.bottomRight()))
        self.currentPoint.setY(rectangle_title.bottom())
    
    def paintIntermediateTitles(self,title):
        """Paint the intermediate titles : years, months and weeks"""
        self.preparePen(15,Qt.SolidLine)
        fontSize = 16
        self.painter.setFont(QFont(self.font,fontSize))
        rectangle_title = QRect(self.currentPoint.x(),self.currentPoint.y(),self.page_rectangle.width(),self.page_rectangle.height()*4/100)
        self.painter.drawText(rectangle_title,Qt.AlignLeft + Qt.AlignVCenter,title)
        self.painter.drawLine(QLineF(rectangle_title.bottomLeft(),rectangle_title.bottomRight())) # changer le style, peut-être l'épaisseur aussi
        self.currentPoint.setY(rectangle_title.bottom())
        
    
    def paintSubtitles(self,title):
        """Paint subtitles : days"""
        self.preparePen(10,Qt.DashLine)
        fontSize = 14
        self.painter.setFont(QFont(self.font,fontSize))
        rectangle_title = QRect(self.currentPoint.x(),self.currentPoint.y(),self.page_rectangle.width(),self.page_rectangle.height()*3/100)
        self.painter.drawText(rectangle_title,Qt.AlignLeft + Qt.AlignVCenter,title)
        self.painter.drawLine(QLineF(rectangle_title.bottomLeft(),rectangle_title.bottomRight())) # changer le style, peut-être l'épaisseur aussi
        self.currentPoint.setY(rectangle_title.bottom())
    
    def paintHeaders(self,headers): # DEPRECATED
        """Paint headers of the widget.
        Headers is a list"""
        size = self.createHRectangles(len(headers),8)
        rectangle_header = QRect(self.currentPoint,size)
        self.painter.setFont(QFont('Arial',15))
        for head in headers:
            self.painter.drawText(rectangle_header,Qt.AlignCenter,head)
            self.currentPoint.setX(self.currentPoint.x() + rectangle_header.width())
            rectangle_header = QRect(self.currentPoint,size)
        self.currentPoint.setX(0)
        self.currentPoint.setY(rectangle_header.bottom())
            
    def paintFeasts(self,headers,data):
        """Paint feasts printed on the screen.
        headers and data are lists of strings."""
        self.preparePen(10,Qt.SolidLine,Qt.darkGray)
        fontSize = 12
        left_center = Qt.AlignLeft + Qt.AlignVCenter + Qt.TextWordWrap + Qt.TextDontClip
        feastFont = QFont(self.font,fontSize)
        feastFont.setBold(True)
        self.painter.setFont(feastFont)
        rectangle_title = QRect(self.currentPoint.x(),self.currentPoint.y(),self.page_rectangle.width(),self.page_rectangle.height()*3/100)
        self.painter.drawText(rectangle_title,left_center,data[0])
        self.painter.drawLine(QLineF(rectangle_title.bottomLeft(),rectangle_title.bottomRight()))
        self.currentPoint.setY(rectangle_title.bottom())
        
        feastFont.setBold(False)
        self.painter.setFont(feastFont)
        rectangle_sizes = [self.createHRectangles(2,3),self.createHRectangles(1,3)]
        last_items = []
        for i, tuple_ in enumerate(zip(headers,data[1:])):
            text = "{} : {}".format(*tuple_)
            if self.painter.boundingRect(QRectF(),Qt.AlignLeft + Qt.AlignVCenter,text).width() > rectangle_sizes[0].width():
                last_items.append((text,self.painter.boundingRect(QRectF(),Qt.AlignLeft + Qt.AlignVCenter,text).width()/rectangle_sizes[1].width()))
                continue
            box = QRect(self.currentPoint,rectangle_sizes[0])
            self.painter.drawText(box,left_center,text)
            if box.left() == self.page_rectangle.left():
                self.currentPoint = box.topRight()
            else:
                self.currentPoint.setX(self.left)
                self.currentPoint.setY(box.bottom())
        self.currentPoint.setX(self.left)
        self.currentPoint.setY(box.bottom())
        if last_items:
            print(last_items)
            last_items.sort(key=lambda x: len(x[0]))
            for elt, rate in last_items:
                box = QRect(self.currentPoint,self.createHRectangles(1,1.5+1.5*math.ceil(rate)))
                self.painter.drawText(box,left_center,elt)
                self.currentPoint = box.bottomLeft()        
        
    def createHRectangles(self,number,percentage):
        """Returns the size of each rectangle.
        QSize is found after dividing self.page_rectangle.width() by number
        and self.page_rectangle.height() by percentage"""
        width = self.page_rectangle.width() / number
        height = percentage * self.page_rectangle.height() / 100
        return QSize(width,height)
    
    def retranslateUI(self):
        self.printDialog.setWindowTitle(_("ExportResults","Print results"))
        self.exportAsPdfTitle = _("ExportResults","Export as PDF")
        self.typeFiles = _("ExportResults",'Documents PDF (*.pdf)')
        self.exportAsSheetTitle = _('ExportResults','Export as spreadsheet')
        self.typeSheetFiles = _("ExportResults",'Documents Excel (*.xls)')
        self.exportAsIcsTitle = _("ExportResults","Export as ICS file")
        self.typeIcsFiles = _("ExportResults","Documents ICS (*.ics)")
    
        
class Onglets(QWidget,SuperTranslator):
    """A class for a tab widget"""
    
    def __init__(self,parent):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.parent = parent
        self.initUI()
        
       
    def initUI(self):
        
        # main widgets
        self.tabs = QTabWidget()
        self.W.tab1 = Unique(self)
        self.W.tabPlus = Multiple(self)
        
        self.tabs.addTab(self.W.tab1,"1")
        self.tabs.addTab(self.W.tabPlus,"+")
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setStatusTip('status')  
        
    def retranslateUI(self):
        SuperTranslator.retranslateUI(self)
        self.setStatusTip(_('Onglets','Research Widget'))
        
class Unique(QWidget,SuperTranslator):
    """A class wich defines a widget with two types of research : for one date and for key-words."""
    
    def __init__(self,parent):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.parent = parent
        self.initUI()
        
    def initUI(self):

        self.day_layout = QVBoxLayout()        
        self.gb_day = QGroupBox("Search for an only date")
        
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setMinimumDate(QDate(1600,1,1))
        self.cal.setMaximumDate(QDate(4100,12,31))

        self.day_layout.addWidget(self.cal)
        self.gb_day.setLayout(self.day_layout)
        
        self.kw_layout = QVBoxLayout()
        self.year_bouton_kw_layout = QHBoxLayout()
        self.rate_result_layout = QHBoxLayout()
        self.max_result_layout = QHBoxLayout()
        
        self.gb_kw = QGroupBox("Search for keywords")
        
        self.keyword = QLineEdit(self)
        self.kw_layout.addWidget(self.keyword)
        
        self.plus = QCheckBox('More results',self)
        self.kw_layout.addWidget(self.plus)

        self.rate_result_label = QLabel("Minimum rate: ")
        self.rate_result_layout.addWidget(self.rate_result_label)
        self.rate_result_label.hide()
        self.rate_result = QSlider(Qt.Horizontal,self) # for martyrology
        self.rate_result.setMinimum(0)
        self.rate_result.setMaximum(100)
        self.rate_result.setValue(80)
        self.rate_result_layout.addWidget(self.rate_result)
        self.rate_result.setVisible(False)

        self.max_result_label = QLabel("Max results: ")
        self.max_result_layout.addWidget(self.max_result_label)
        self.max_result_label.hide()
        self.max_result = QSpinBox(self) # for martyrology
        self.max_result.setMinimum(1)
        self.max_result.setMaximum(366)
        self.max_result.setValue(5)
        self.max_result_layout.addWidget(self.max_result)
        self.max_result.setVisible(False)
        
        self.spinbox = YearSpinbox()        
        self.kw_bouton = QPushButton('kw_button',self)
        
        self.year_bouton_kw_layout.addWidget(self.spinbox)
        self.year_bouton_kw_layout.addWidget(self.kw_bouton)
        
        self.kw_layout.addLayout(self.rate_result_layout)
        self.kw_layout.addLayout(self.max_result_layout)
        self.kw_layout.addLayout(self.year_bouton_kw_layout) 
        self.gb_kw.setLayout(self.kw_layout)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.gb_day)
        self.layout.addWidget(self.gb_kw)
        self.layout.addStretch(1)
        
        self.setLayout(self.layout)
        
    def retranslateUI(self):
        SuperTranslator.retranslateUI(self)

        self.cal.setLocale(self.locale())
        self.cal.setFirstDayOfWeek(7)
        
        self.gb_day.setTitle(_('Unique','Search for an only day'))
        self.gb_kw.setTitle(_('Unique',"Search by keywords"))
        self.rate_result_label.setText(_("Unique","Minimum rate: "))
        self.max_result_label.setText(_("Unique","Maximum results: "))
        self.keyword.setPlaceholderText(_("Unique","Enter keywords here"))
        self.plus.setText(_('Unique','More results'))
        self.kw_bouton.setText(_('Unique','OK'))
        
        
class Multiple(QWidget,SuperTranslator):
    """A class which defines widgets with multiple results : research by week, month, year, or arbitrary"""
    
    def __init__(self,parent):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.parent = parent
        self.initUI()
        
    def initUI(self):   
        #week
        self.gb_week = QGroupBox("Search for a whole week")
        self.week_layout = QVBoxLayout()
        self.week_top_layout = QHBoxLayout()
        self.week_bottom_layout = QHBoxLayout()
        self.wy_spinbox = YearSpinbox()
        self.wy_spinbox.valueChanged.connect(self.change_weeks)
        self.monthweek_combo = QComboBox()
        self.monthweek_combo.currentIndexChanged.connect(self.change_weeks)
        self.week_combo = QComboBox()
        self.bt_week = QPushButton("OK")
        self.week_top_layout.addWidget(self.wy_spinbox)
        self.week_top_layout.addWidget(self.monthweek_combo)
        self.week_bottom_layout.addWidget(self.week_combo)
        self.week_bottom_layout.addWidget(self.bt_week)
        self.week_layout.addLayout(self.week_top_layout)
        self.week_layout.addLayout(self.week_bottom_layout)
        self.gb_week.setLayout(self.week_layout)
        #month
        self.gb_month = QGroupBox("Search for a whole month")
        self.month_layout = QHBoxLayout()
        self.my_spinbox = YearSpinbox()
        self.month_combo = QComboBox()
        self.bt_month = QPushButton("OK")        
        self.month_layout.addWidget(self.my_spinbox)
        self.month_layout.addWidget(self.month_combo)
        self.month_layout.addWidget(self.bt_month)
        self.gb_month.setLayout(self.month_layout)
        #year
        self.gb_year = QGroupBox("Search for a whole year")
        self.yy_spinbox = YearSpinbox()
        self.bt_year = QPushButton("OK")
        self.year_layout = QHBoxLayout()
        self.year_layout.addWidget(self.yy_spinbox)
        self.year_layout.addWidget(self.bt_year)
        self.gb_year.setLayout(self.year_layout)      
        #arbitrary
        self.gb_arbritrary = QGroupBox("Search for arbitrary dates")
        self.frome_label = QLabel("frome label",self)
        self.frome = QDateEdit()
        self.frome.setMinimumDate(QDate(1600,1,1))
        self.frome.setMaximumDate(QDate(4100,12,31)) # set to current
        self.frome.setDate(current)
        self.frome.setCalendarPopup(True)
        self.frome.dateChanged.connect(self.isgreater)
        self.to_label = QLabel("to label",self)
        self.to = QDateEdit()
        self.to.setMinimumDate(QDate(1600,1,1))
        self.to.setMaximumDate(QDate(4100,12,31))
        self.to.setDate(current)
        self.to.setCalendarPopup(True)
        self.to.dateChanged.connect(self.isgreater)
        self.arbitrary_layout = QVBoxLayout()
        self.bt_arbitrary = QPushButton("OK")
        self.arbitrary_layout.addWidget(self.frome_label)
        self.arbitrary_layout.addWidget(self.frome)
        self.arbitrary_layout.addWidget(self.to_label)
        self.arbitrary_layout.addWidget(self.to)
        self.arbitrary_layout.addWidget(self.bt_arbitrary)
        self.gb_arbritrary.setLayout(self.arbitrary_layout)
        #main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.gb_week)
        self.layout.addWidget(self.gb_month)
        self.layout.addWidget(self.gb_year)
        self.layout.addWidget(self.gb_arbritrary)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
        
    def retranslateUI(self):
        SuperTranslator.retranslateUI(self)

        self._week_word = _("Multiple","week")
        self._ordinary_numbers = (
                _("Multiple","First"),
                _("Multiple","Second"),
                _("Multiple","Third"),
                _("Multiple","Fourth"),
                _("Multiple","Fifth"),
                _("Multiple","Sixth")) # useful for gender

        # set ok buttons text
        OK = _("Multiple","OK")
        for button in (self.bt_week,self.bt_month,self.bt_year,self.bt_arbitrary):
            button.setText(OK)
        
        # months of week widget
        self.gb_week.setTitle(_("Multiple","Search for a whole week"))
        month_id = self.monthweek_combo.currentIndex()
        self.monthweek_combo.clear()
        for month in self.months_translated0: 
            self.monthweek_combo.addItem(month)
        if month_id > 0:
            self.monthweek_combo.setCurrentIndex(month_id)

        
        self.gb_month.setTitle(_("Multiple","Search for a whole month"))
        month_id = self.month_combo.currentIndex()
        self.month_combo.clear()
        for month in self.months_translated0:
            self.month_combo.addItem(month) # set current in main initUI
        if month_id > 0:
            self.month_combo.setCurrentIndex(month_id)
        
        self.gb_year.setTitle(_("Multiple","Search for a whole year"))
        
        self.gb_arbritrary.setTitle(_("Multiple","Search for arbitrary dates"))
        self.frome_label.setText(_("Multiple","Select the earlier date : "))
        self.to_label.setText(_("Multiple","Select the later date : "))
        
    def isgreater(self,date):
        """This method tests wether 'frome' date is greater than 'to' date, and sets dates if necessary"""
        if self.frome.date() > self.to.date():
            if date == self.frome.date():
                self.frome.setDate(self.to.date())
            else:
                self.to.setDate(self.frome.date())
                
    def change_weeks(self):
        """This method changes the week combo and set it to current week if possible"""
        if self.monthweek_combo.count() == 0:
            return
        self.week_combo.clear()
        month_requested = self.monthweek_combo.currentIndex() + 1
        year_requested = self.wy_spinbox.value()
        month = calendrier.monthdayscalendar(year_requested,month_requested)
        for i, name in zip(month, self._ordinary_numbers):
            self.week_combo.addItem("{} {}".format(name,self._week_word)) 

        if year_requested == current.year() and month_requested == current.month():
            for i, week in enumerate(month):
                if current.day() in week:
                    self.week_combo.setCurrentIndex(i)
                    break
                
class Tree(QTreeWidget,SuperTranslator):
    """A class which defines the main widget used with multiple days"""
    
    def __init__(self,parent,data,Annee,pal=False):
        """Inits the tree.
        data is a list of lists of feasts.
        pal determines wether or not pro aliquibus feasts are included."""
        QWidget.__init__(self)
        SuperTranslator.__init__(self)

        self.translateStrings()
        self.parent = parent # mainWindow
        self.lang = parent.lang
        self.Annee=Annee  
        self.pal = pal
        self.W.itemsCreator = ItemsCreator(self)
        self.initUI(data)
        self.retranslateUI()
        for i in range(8):
            self.resizeColumnToContents(i)
        self.header().setStretchLastSection(True)
        self.itemDoubleClicked.connect(self.url)
        
    
    def initUI(self,data):
        self.setColumnCount(7)
        self.populateTree(data,self.invisibleRootItem())
        
    def populateTree(self,data,parent):
        """A function which populates the QTreeWidget"""
        for key, item in sorted(data.items()):
            if isinstance(item,list):
                item = { i:elt for i,elt in enumerate(item)}
            if isinstance(item,dict):
                if isinstance(key,tuple):
                    if key[1] == 'week':
                        key = """{} {}""".format(
                                self.ordinary_numbers_translated0[key[0]],
                                self.week_translated)
                    else:
                        key = self.months_translated1[key[0]].capitalize()
                elif isinstance(key,int):
                    key = str(key)
                else:
                    #key = officia.affiche_jour(key,self.lang).capitalize()
                    key = self.localizedDate(day=key).capitalize()
                child = QTreeWidgetItem(parent,[key])
                child.setExpanded(True)
                self.populateTree(item,child)
            else:
                if not item.pal or item.pal and self.pal:
                    self.W.itemsCreator.createLine(item,parent)

    def url(self,child):
        """Opens a new tab in default webbrowser
        at the url of child"""
        webbrowser.open_new_tab(child.url)

    def translateStrings(self):
        """Translate some strings"""
        self.week_translated = _("Tree","week")

        
    def retranslateUI(self):
        SuperTranslator.retranslateUI(self)
        self.setHeaderLabels([_("Tree","Date/Name"),_('Tree','Status'),_("Tree","Class"),_("Tree","Colour"),_("Tree","Temporal/Sanctoral"),_("Tree","Time"),_('Tree','Proper'),_('Tree','Station'),_('Tree','Addendum')])
        
class Table(QTableWidget,SuperTranslator):

    def __init__(self,parent,liste,Annee,inverse=False,pal=False):
        """Set the table.
        liste is a list of feasts.
        Annee is a annus.LiturgicalCalendar.
        inverse determines wether keyword research is set (True) or not (False)
        pal determines wether Masses Pro Aliquibus Locis are requested (True) or not (False)
        """

        QTableWidget.__init__(self)
        SuperTranslator.__init__(self)

        self.parent = parent
        self.lang = parent.lang
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers) # no edition possible
        self.cellDoubleClicked.connect(self.url)

        if not pal:
            #Masses pro aliquibus locis are deleted if not requested
            liste = [feast for feast in liste if not feast.pal]
        self.nbColumn = 10 
        self.setColumnCount(self.nbColumn)
        self.setRowCount(len(liste))
        self.inverse = inverse
        self.retranslateUI()
        self.fontOmitted = QFont()
        self.fontOmitted.setItalic(True)
        
        if self.inverse:
            self.name_pos, self.date_pos = 0, 1
        else:
            self.name_pos, self.date_pos = 1, 0
        self.W.itemsCreator = ItemsCreator(self)
        for i, elt in enumerate(liste):
            self.W.itemsCreator.createLine(elt,itemLine=i)
            
        for i in range(self.nbColumn):
            self.resizeColumnToContents(i)
        self.horizontalHeader().setStretchLastSection(True)

    def url(self,row: int):
        """Opens a new tab in default webbrowser
        for requested feast."""
        child = self.item(row,0)
        webbrowser.open_new_tab(child.url)
        
        
    def retranslateUI(self):
        self.tempOrSanct = {True:_('Table','Temporal'),False:_('Table','Sanctoral')}
        if self.inverse:
            first_item = _("Table",'Name')
            second_item = _("Table",'Date')
        else:
            first_item = _("Table",'Date')
            second_item = _("Table",'Name')
        self.setHorizontalHeaderLabels([first_item,second_item,_('Table','Status'),_("Table",'Class'),_("Table",'Colour'),_("Table",'Temporal/Sanctoral'),_("Table",'Time'),_("Table",'Proper'),_('Table','Station'),_('Table','Addendum')])
        
        
class ItemsCreator(SuperTranslator):
    """Convenient class for printing data in both Table and Tree Widgets"""
    fontOmitted = QFont() # font used for feasts omitted
    fontOmitted.setItalic(True)
    
    
    def __init__(self,parent):
        SuperTranslator.__init__(self)
        self.parent = parent
        self.lang = parent.lang
        self.mainWindow = parent.parent
        self.retranslateUI()
        
    def createLine(self,data,itemParent=None,itemLine=None):
        """Creates a line of results in Tree or in Table"""
        texts = self.presentData(data)
        if isinstance(self.parent,Tree):
            child = QTreeWidgetItem(itemParent,[texts[0],*texts[2]])
            child.url = data.link
            if data.omission:
                for i in range(8):
                    child.setFont(i,self.fontOmitted)
        else:
            self.parent.setItem(itemLine,self.parent.name_pos,QTableWidgetItem(texts[0]))
            self.parent.setItem(itemLine,self.parent.date_pos,QTableWidgetItem(texts[1]))
            for i,elt in enumerate(texts[2]):
                self.parent.setItem(itemLine,i+2,QTableWidgetItem(elt))
            self.parent.item(itemLine,0).url = data.link
            if data.omission:
                for column in range(self.parent.nbColumn):
                    self.parent.item(itemLine,column).setFont(self.fontOmitted)
        
    def presentData(self,data):
        """Presents the data as they will be printed on the screen"""
        name = data.nom[self.lang]
        date = str(data.date)
        date = self.localizedDate(day=data.date)
        if data.celebree:
            status = _('ItemsCreator','Celebrated')
        elif data.commemoraison and data.peut_etre_celebree:
            status = _("ItemsCreator","Can be celebrated or commemorated")
        elif data.commemoraison:
            status = _('ItemsCreator','Commemorated')
        elif data.omission:
            status = _('ItemsCreator','Omitted')
        elif data.peut_etre_celebree:
            status = _("ItemsCreator","Can be celebrated")
        if data.transferee:
            status += _("ItemsCreator"," & transferred from {}").format(self.localizedDate(day=data.date_originelle))
        degree = self.classes[data.degre]
        colour = officia.liturgical_colour(data,self.lang).capitalize() # english ???
        temporsanct = self.tempOrSanct[data.temporal]
        time = first_upper(officia.affiche_temps_liturgique(data,self.lang))
        proper = self.mainWindow.propersDict[data.propre]
        station = data.__dict__.get('station',{self.lang:''})[self.lang]
        addendum = data.addendum.get(self.lang,'')
        return name, date, (status, degree, colour, temporsanct, time, proper, station, addendum)
        
    def retranslateUI(self):
        self.tempOrSanct = {True:_('ItemsCreator','Temporal'),False:_('ItemsCreator','Sanctoral')}
        self.classes = {1:_('ItemsCreator','First Class'),
                        2:_('ItemsCreator','Second Class'),
                        3:_('ItemsCreator','Third Class'),
                        4:_('ItemsCreator','Fourth Class'),
                        5:_('ItemsCreator','Commemoration'),
                        6:_('ItemsCreator','Mass Pro Aliquibus Locis'),}
       
        
    
