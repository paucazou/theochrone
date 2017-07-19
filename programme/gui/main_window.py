#!/usr/bin/python3
# -*-coding:Utf-8 -*
# Deus in adjutorium meum intende

import calendar
import datetime
import os.path
import sys

chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/..')
sys.path.append(programme)
sys.path.append(chemin)
import adjutoria
import annus
import officia
import settings
os.chdir(chemin)

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QCoreApplication, QDate, QLocale, QPoint, QRect, Qt, QTranslator
from PyQt5.QtGui import QFont, QIcon, QPainter, QTextDocument
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QAction, QApplication, QCalendarWidget, QCheckBox, QComboBox, QDateEdit, QDockWidget, QFileDialog, QGroupBox, QHBoxLayout, QMainWindow, QLabel, QLineEdit, QPushButton, QSlider, QSpinBox, QStyle, QTableWidget, QTableWidgetItem, QTabWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from translation import *


_ = QCoreApplication.translate # a name more convenient
current = QDate().currentDate()
calendrier = calendar.Calendar(firstweekday=6)
months_tuple = ('','janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre')
week_number = ("Première","Deuxième","Troisième","Quatrième","Cinquième","Sixième") # TODO TRANSLATION ?
first_upper = lambda x : x[0].upper() + x[1:]
            
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
        self.translator.load(QLocale(),"gui",'.','./i18n','.qm') # TODO : sélection de la langue dans cet ordre : settings, locale, puis choix.
        self.execute = Main(args)

class Main(QMainWindow,SuperTranslator):
    """Main window"""
    def __init__(self,args):
        """Function which initializes the main window"""
        
        QMainWindow.__init__(self)
        SuperTranslator.__init__(self)
        self.Annee = annus.LiturgicalCalendar()
        self.ferryman = ExportResults(self)
        self.actions()
        self.initUI()
        self.processCommandLineArgs(args)
        
        self.W.onglets.W.tab1.cal.clicked[QDate].connect(self.useDate)
        self.W.onglets.W.tab1.kw_bouton.clicked.connect(self.useKeyWord)
        self.W.onglets.W.tab1.keyword.returnPressed.connect(self.useKeyWord)
        self.W.onglets.W.tab1.spinbox.editingFinished.connect(self.useKeyWord)
        
        self.W.onglets.W.tabPlus.bt_week.clicked.connect(self.useWeek)
        self.W.onglets.W.tabPlus.wy_spinbox.editingFinished.connect(self.useWeek)
        
        self.W.onglets.W.tabPlus.bt_month.clicked.connect(self.useMonth)
        self.W.onglets.W.tabPlus.my_spinbox.editingFinished.connect(self.useMonth)
        
        self.W.onglets.W.tabPlus.yy_spinbox.editingFinished.connect(self.useYear)
        self.W.onglets.W.tabPlus.bt_year.clicked.connect(self.useYear)
        
        self.W.onglets.W.tabPlus.bt_arbitrary.clicked.connect(self.useArbitrary)
        self.W.onglets.W.tabPlus.to.editingFinished.connect(self.useArbitrary)
        self.W.onglets.W.tabPlus.frome.editingFinished.connect(self.useArbitrary)
        
    def processCommandLineArgs(self,args):
        reverse, debut, fin, plus = args
        if reverse != 1:
            self.W.onglets.W.tab1.keyword.setText(' '.join(reverse))
            self.W.onglets.W.tab1.spinbox.setValue(debut.year)
            if plus:
                self.W.onglets.W.tab1.plus.setChecked(True)
            self.useKeyWord()
        elif debut == fin != current.toPyDate():
            self.useDate(QDate(debut.year,debut.month,debut.day))
        elif debut != fin:
            self.W.onglets.W.tabPlus.frome.setDate(QDate(debut.year,debut.month,debut.day))
            self.W.onglets.W.tabPlus.to.setDate(QDate(fin.year,fin.month,fin.day))
            self.useArbitrary()
            self.W.onglets.tabs.setCurrentIndex(1)
        
    def menu(self):
        """A function which describes the menubar of the main window"""
        menubar = self.menuBar()
        
        # File menu
        self.fileMenu = menubar.addMenu('file')
        self.fileMenu.addAction(self.settingsAction)
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.exportPDF)
        self.fileMenu.addAction(self.exitAction)
        
        # Edit menu
        self.editMenu = menubar.addMenu('edit')
        
        # Language menu (change on the fly)
        self.languageMenu = menubar.addMenu('language')
        self.languageMenu.addAction(self.chooseLanguageLatin)
        self.languageMenu.addAction(self.chooseLanguageFrench)
        self.languageMenu.addAction(self.chooseLanguageEnglish)
        
        # Help menu
        self.helpMenu = menubar.addMenu('help')
        
    def actions(self):
        """A function which defines actions in the main window"""
        
        #File
        # Settings
        self.settingsAction = QAction(QIcon('icons/settings.png'),'settings',self) # icons https://www.iconfinder.com/icons/353407/cog_settings_icon#size=128
        self.settingsAction.triggered.connect(self.openSettings)
        self.settingsAction.setShortcut('Ctr+S')
        # Print
        self.printAction = QAction(QIcon('icons/print.png'),'print',self) # https://www.iconfinder.com/icons/392497/print_printer_printing_icon#size=128
        self.printAction.setShortcut('Ctrl+P')
        self.printAction.triggered.connect(self.printChildren)
        # PDF
        self.exportPDF = QAction(QIcon('icons/pdf.png'),'export as PDF',self) # https://www.iconfinder.com/icons/83290/file_pdf_icon#size=32
        self.exportPDF.triggered.connect(self.ferryman.exportAsPDF)
        self.exportPDF.setShortcut('Ctrl+E')
        # Exit
        self.exitAction = QAction(QIcon('icons/exit.png'),'exit_name',self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)
        
        # Languages
        ## Latin
        self.chooseLanguageLatin = QAction(QIcon('icons/latin.png'),'choose_latin',self) # à lier dans la classe App pour changer de langue
        ## French
        self.chooseLanguageFrench = QAction(QIcon('icons/french.png'),'choose_french',self)
        ## English
        self.chooseLanguageEnglish = QAction(QIcon('icons/english.png'),'choose_english',self)
                                           
        
    def initUI(self):
        """A function which defines widgets and main features of the window"""
        
        # widgets
        # main widget
        self.arbre = QTreeWidget()
        # widgets on the right
        self.rightDock = QDockWidget('right_dock',self)
        self.W.onglets = Onglets()
        self.rightDock.setWidget(self.W.onglets)
        self.addDockWidget(Qt.RightDockWidgetArea,self.rightDock)
        
        # menu
        self.menu()        
        
        # statusbar
        self.statusBar()
        
        # main features
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight,Qt.AlignCenter,self.size(),App.desktop().availableGeometry()))
        self.retranslateUI() # voir si on ne la met pas carrément dans l'app, qui hériterait elle aussi de SuperTranslator
        # default settings
        self.useDate(current)
        self.W.onglets.W.tabPlus.month_combo.setCurrentIndex(current.month() - 1)
        self.W.onglets.W.tabPlus.monthweek_combo.setCurrentIndex(current.month() - 1)
        self.W.onglets.W.tabPlus.change_weeks()
        self.show()
        
    def retranslateUI(self):
        SuperTranslator.retranslateUI(self)
        
        #menu
        self.fileMenu.setTitle(_('Main','File'))
        self.editMenu.setTitle(_('Main','Edit'))
        self.languageMenu.setTitle(_('Main','Language'))
        self.helpMenu.setTitle(_('Main','Help'))
        
        #actions
        self.settingsAction.setText(_('Main','Settings'))
        
        self.printAction.setText(_('Main','Print'))
        self.exportPDF.setText(_('Main','Export as PDF'))
        
        self.exitAction.setText(_('Main','Exit'))
        self.exitAction.setStatusTip(_('Main','Exit the app'))
        
        self.chooseLanguageLatin.setText(_('Main','Latin'))
        self.chooseLanguageFrench.setText(_('Main','French'))
        self.chooseLanguageEnglish.setText(_('Main','English'))
        
        #initUI
        #widgets on the right
        self.rightDock.setWindowTitle(_('Main','Research'))
        
    def openSettings(self): # passer un argument concernant la langue choisie
        self.W.settings = settings.SettingsWindow()
        
    def useDate(self,date):
        self.setWindowTitle('Theochrone - ' + date.toString())
        debut = fin = date.toPyDate()
        self.Annee(debut.year)
        selection = self.Annee[debut]
        self.tableau = Table(selection,self.Annee)
        self.setCentralWidget(self.tableau)
        officia.pdata(write=True,history='dates',debut=debut,fin=fin)
        
    def useKeyWord(self):
        keyword = self.W.onglets.W.tab1.keyword.text()
        if keyword == '':
            return
        self.setWindowTitle('Theochrone - ' + keyword)
        annee = self.W.onglets.W.tab1.spinbox.value()
        debut, fin = datetime.date(annee,1,1), datetime.date(annee, 12,31)
        self.Annee(debut.year)
        if self.W.onglets.W.tab1.plus.isChecked():
            plus = True
        else:
            plus = False
        selection = officia.inversons(keyword,self.Annee,debut,fin,exit=False,plus=plus) # plantage en cas de recherche sans résultat...
        self.W.tableau = Table(selection,self.Annee,True)
        self.setCentralWidget(self.W.tableau)
        officia.pdata(write=True,history='reverse',debut=debut,fin=fin,keywords=[keyword])
            
    def useWeek(self):
        tab=self.W.onglets.W.tabPlus
        year = tab.wy_spinbox.value()
        month = tab.monthweek_combo.currentIndex() + 1
        week = tab.week_combo.currentIndex()
        self.Annee(year)
        WEEK = self.Annee.weekmonth(year,month,week)
        self.W.arbre = Tree(WEEK,self.Annee)
        self.setCentralWidget(self.W.arbre)
        if months_tuple[month][0] in ('a','o'):
            preposition = "d'"
        else:
            preposition = "de "
        self.setWindowTitle('Theochrone - {} semaine {}{} {}'.format(
            week_number[week], preposition,
            months_tuple[month],str(year)))
        debut, fin = sorted(WEEK)[0], sorted(WEEK)[-1]
        officia.pdata(write=True,history='dates',debut=debut,fin=fin,semaine_seule=True)
        
    def useMonth(self):
        tab = self.W.onglets.W.tabPlus
        year = tab.my_spinbox.value()
        month = tab.month_combo.currentIndex() + 1
        self.Annee(year)
        MONTH = self.Annee.listed_month(year, month)
        self.W.arbre = Tree(MONTH,self.Annee)
        self.setCentralWidget(self.W.arbre)
        self.setWindowTitle('Theochrone - {} {}'.format(months_tuple[month].capitalize(),str(year)))
        #debut = next(iter(sorted(next(iter(MONTH.values()))))) # Do you know this is horrible and useless ?
        debut = datetime.date(year,month,1)
        fin_day = calendar.monthrange(year,month)[1]
        fin = datetime.date(year,month,fin_day)
        officia.pdata(write=True,history='dates',debut=debut,fin=fin,mois_seul=True)
        
    def useYear(self):
        tab = self.W.onglets.W.tabPlus
        year = tab.yy_spinbox.value()
        self.Annee(year)
        YEAR = self.Annee.listed_year(year)
        self.W.arbre = Tree(YEAR,self.Annee)
        self.setCentralWidget(self.W.arbre)
        self.setWindowTitle('Theochrone - {}'.format(str(year)))
        officia.pdata(write=True,history='dates',debut=datetime.date(year,1,1),fin=datetime.date(year,12,31),annee_seule=True)
        
    def useArbitrary(self):
        tab = self.W.onglets.W.tabPlus
        debut = tab.frome.date().toPyDate()
        fin = tab.to.date().toPyDate()
        self.Annee(debut.year,fin.year)
        RANGE = self.Annee.listed_arbitrary(debut,fin)
        self.W.arbre = Tree(RANGE,self.Annee)
        self.setCentralWidget(self.W.arbre)
        self.setWindowTitle('Theochrone - du {} au {}'.format(tab.frome.date().toString(),
                                                              tab.to.date().toString()))
        officia.pdata(write=True,history='dates',debut=debut,fin=fin,fromto=True)
        
    def exportAsPDF(self):
        personal_directory = os.path.expanduser('~')
        dialog = QFileDialog.getSaveFileName(self,'Export as PDF',personal_directory,'Documents PDF (*.pdf)')
        if dialog[0]:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(dialog[0])
            self.centralWidget().render(printer) # Créer plutôt un modèle d'impression à partir des données de base, avec du texte brut. TODO
            
    def printResults(self):
        printer = QPrinter(QPrinter.HighResolution)
        printDialog = QPrintDialog(printer,self)
        printDialog.setWindowTitle(_("Main","Print results"))
        if printDialog[0]:
            #print
            painter = QPainter()
            painter.begin(printer)
            while True:
                printer.newPage()
            painter.end()
            
    def printChildren(self,parent=None):
        if not parent:
            parent = self.centralWidget().invisibleRootItem()
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.columnCount() == 1:
                print(child.text(0))
            else:
                print(*[child.text(j) for j in range(child.columnCount())])
            if child.childCount():
                self.printChildren(child)
        
class ExportResults(SuperTranslator):
    """Manage the exports in other formats.
    For now : PDF, print"""
    
    def __init__(self,parent):
        SuperTranslator.__init__(self)
        self.parent = parent
        self.printer = QPrinter(QPrinter.HighResolution)
        self.painter = QPainter()
        self.printDialog = QPrintDialog(self.printer,self.parent)
        self.personal_directory = os.path.expanduser('~')
        self.retranslateUI()
        
    def exportToPrinter(self):
        if self.printDialog.exec():
            print('oui')
            
    def exportAsPDF(self):
        dialog = QFileDialog.getSaveFileName(self.parent,self.exportAsPdfTitle,self.personal_directory,self.typeFiles)
        if dialog[0]:
            self.printer.setOutputFormat(QPrinter.PdfFormat)
            self.printer.setOutputFileName(dialog[0])
            self.paintController()
            
    def paintController(self):
        """Manage the main painting"""
        self.page_rectangle = self.printer.pageRect()
        self.painter.begin(self.printer)
        self.paintMainTitle()
        self.painter.end()
    
    def paintMainTitle(self):
        """Paint the main title, ie the research keywords"""
        title = self.parent.windowTitle()
        rectangle_title = QRect(0,0,self.page_rectangle.right()-self.page_rectangle.left(),self.page_rectangle.height()/10)
        self.painter.drawRect(rectangle_title)
        self.painter.setFont(QFont('Arial',30)) # taille de la police à modifier selon le cas ? -> certains titres sont trop grands
        
        self.painter.drawText(rectangle_title,Qt.AlignCenter,title)
    
    def paintIntermediateTitles(self):
        """Paint the intermediate titles : years, months and weeks"""
        pass
    
    def paintSubtitles(self):
        """Paint subtitles : days"""
        pass
    
    def paintHeaders(self):
        """Paint headers of the widget"""
        pass
    
    def paintFeasts(self):
        """Paint feasts printed on the screen"""
        pass
    
    def retranslateUI(self):
        self.printDialog.setWindowTitle(_("ExportResults","Print results"))
        self.exportAsPdfTitle = _("ExportResults","Export as PDF")
        self.typeFiles = _("ExportResults",'Documents PDF (*.pdf)')
    
        
class Onglets(QWidget,SuperTranslator):
    """A class for a tab widget"""
    
    def __init__(self):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.initUI()
        
       
    def initUI(self):
        
        # main widgets
        self.tabs = QTabWidget()
        self.W.tab1 = Unique()
        self.W.tabPlus = Multiple()
        
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
    
    def __init__(self):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.initUI()
        
    def initUI(self):

        self.day_layout = QVBoxLayout()        
        self.gb_day = QGroupBox("Search for an only date")
        
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setFirstDayOfWeek(0)
        self.cal.setMinimumDate(QDate(1600,1,1))
        self.cal.setMaximumDate(QDate(4100,12,31))

        self.day_layout.addWidget(self.cal)
        self.gb_day.setLayout(self.day_layout)
        
        self.kw_layout = QVBoxLayout()
        self.slider_layout = QHBoxLayout()
        
        self.gb_kw = QGroupBox("Search for keywords")
        
        self.keyword = QLineEdit(self)
        self.kw_layout.addWidget(self.keyword)
        
        self.plus = QCheckBox('More results',self)
        self.kw_layout.addWidget(self.plus)
        
        self.spinbox = YearSpinbox()        
        self.kw_bouton = QPushButton('kw_button',self)
        
        self.slider_layout.addWidget(self.spinbox)
        self.slider_layout.addWidget(self.kw_bouton)
        
        self.kw_layout.addLayout(self.slider_layout) 
        self.gb_kw.setLayout(self.kw_layout)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.gb_day)
        self.layout.addWidget(self.gb_kw)
        self.layout.addStretch(1)
        
        self.setLayout(self.layout)
        
    def retranslateUI(self):
        SuperTranslator.retranslateUI(self)
        
        self.gb_day.setTitle(_('Unique','Search for an only day'))
        self.gb_kw.setTitle(_('Unique',"Search by keywords"))
        self.keyword.setPlaceholderText(_("Unique","Enter keywords here"))
        self.plus.setText(_('Unique','More results'))
        self.kw_bouton.setText(_('Unique','OK'))
        
        self.cal.setLocale(QLocale()) # à mettre dans la toute première fonction
        
class Multiple(QWidget,SuperTranslator):
    """A class which defines widgets with multiple results : research by week, month, year, or arbitrary"""
    
    def __init__(self):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
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
        self.monthweek_combo.activated.connect(self.change_weeks)
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
        months = (_("Multiple","January"),_("Multiple","February"),_("Multiple","March"),_("Multiple","April"),_("Multiple","May"),_("Multiple","June"),
                     _("Multiple","July"),_("Multiple","August"),_("Multiple","September"),_("Multiple","October"),_("Multiple","November"),_("Multiple","December"))
        
        self.gb_week.setTitle(_("Multiple","Search for a whole week"))
        for month in months:
            self.monthweek_combo.addItem(month)
        self.weeknames = (_("Multiple","First"),_("Multiple","Second"),_("Multiple","Third"),_("Multiple","Fourth"),_("Multiple","Fifth"),_("Multiple","Sixth"))
        
        self.gb_month.setTitle(_("Multiple","Search for a whole month"))
        for month in months:
            self.month_combo.addItem(month) # set current in main initUI
        
        self.gb_year.setTitle(_("Multiple","Search for a whole year"))
        self.bt_year.setText(_("Multiple","OK"))
        
        self.gb_arbritrary.setTitle(_("Multiple","Search for arbitrary dates"))
        self.frome_label.setText(_("Multiple","Select the earlier date : "))
        self.to_label.setText(_("Multiple","Select the later date : "))
        self.bt_arbitrary.setText(_("Multiple","OK"))
        
    def isgreater(self,date):
        """This method tests wether 'frome' date is greater than 'to' date, and sets dates if necessary"""
        if self.frome.date() > self.to.date():
            if date == self.frome.date():
                self.frome.setDate(self.to.date())
            else:
                self.to.setDate(self.frome.date())
                
    def change_weeks(self):
        """This method changes the week combo and set it to current week if possible"""
        self.week_combo.clear()
        month_requested = self.monthweek_combo.currentIndex() + 1
        year_requested = self.wy_spinbox.value()
        month = calendrier.monthdayscalendar(year_requested,month_requested)
        for i, name in zip(month, self.weeknames):
            self.week_combo.addItem("{} week".format(name))
        if year_requested == current.year() and month_requested == current.month():
            for i, week in enumerate(month):
                if current.day() in week:
                    self.week_combo.setCurrentIndex(i)
                    break
                
class Tree(QTreeWidget,SuperTranslator):
    """A class which defines the main widget used with multiple days"""
    
    depth = lambda self,L: isinstance(L, list) and max(map(self.depth, L),default=0)+1 #http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to 
    def __init__(self,data,Annee):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.Annee=Annee  
        self.W.itemsCreator = ItemsCreator(self)
        self.initUI(data)
        self.retranslateUI()
        for i in range(8):
            self.resizeColumnToContents(i)
        self.header().setStretchLastSection(True)
        
    
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
                        key = """{} semaine""".format(week_number[key[0]])
                    else:
                        key = months_tuple[key[0]].capitalize()
                elif isinstance(key,int):
                    key = str(key)
                else:
                    key = officia.affiche_jour(key,'francais').capitalize()
                child = QTreeWidgetItem(parent,[key])
                child.setExpanded(True)
                self.populateTree(item,child)
            else:
                """elt = item
                if elt.temporal:
                    temps = 'Temporal'
                else:
                    temps = 'Sanctoral'
                child=QTreeWidgetItem(parent,[elt.nom['francais'],str(elt.degre),elt.couleur,officia.affiche_temps_liturgique(elt,'francais').capitalize(),temps])
                """
                self.W.itemsCreator.createLine(item,parent)
        
    def retranslateUI(self):
        SuperTranslator.retranslateUI(self)
        self.setHeaderLabels([_("Tree","Date/Name"),_('Tree','Status'),_("Tree","Class"),_("Tree","Colour"),_("Tree","Temporal/Sanctoral"),_("Tree","Time"),_('Tree','Station')])
        
class Table(QTableWidget,SuperTranslator):

    def __init__(self,liste,Annee,inverse=False):
        QTableWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.nbColumn = 8
        self.setColumnCount(self.nbColumn)
        self.setRowCount(len(liste))
        self.inverse = inverse
        self.retranslateUI()
        self.fontOmitted = QFont()
        self.fontOmitted.setItalic(True)
        self.tempOrSanct = {True:_('Table','Temporal'),False:_('Table','Sanctoral')}
        self.classes = {1:_('Table','First Class'),
                        2:_('Table','Second Class'),
                        3:_('Table','Third Class'),
                        4:_('Table','Fourth Class'),
                        5:_('Table','Commemoration'),}
        
        if self.inverse:
            self.name_pos, self.date_pos = 0, 1
        else:
            self.name_pos, self.date_pos = 1, 0
        self.W.itemsCreator = ItemsCreator(self)
        for i, elt in enumerate(liste):
            self.W.itemsCreator.createLine(elt,itemLine=i)
            """self.setItem(i,name_pos,QTableWidgetItem(elt.nom['francais']))
            self.setItem(i,date_pos,QTableWidgetItem(str(elt.date)))
            self.setItem(i,3,QTableWidgetItem(self.classes[elt.degre]))
            self.setItem(i,4,QTableWidgetItem(elt.couleur.capitalize()))
            self.setItem(i,5,QTableWidgetItem(self.tempOrSanct[elt.temporal]))
            self.setItem(i,6,QTableWidgetItem(first_upper(officia.affiche_temps_liturgique(elt,'francais'))))
            if elt.__dict__.get('station',False):
                station=elt.station['francais']
            else:
                station=''
            self.setItem(i,7,QTableWidgetItem(station))
            if elt.celebree:
                status = _('Table','Celebrated')
            elif elt.commemoraison and elt.peut_etre_celebree:
                status = _("Table","Can be celebrated or commemorated")
            elif elt.commemoraison:
                status = _('Table','Commemorated')
            elif elt.omission:
                status = _('Table','Omitted')
            elif elt.peut_etre_celebree:
                status = _("Table","Can be celebrated")
            
                
            self.setItem(i,2,QTableWidgetItem(status))
            if elt.omission:
                for column in range(self.nbColumn):
                    self.item(i,column).setFont(self.fontOmitted)"""
            
            
        for i in range(self.nbColumn):
            self.resizeColumnToContents(i)
        self.horizontalHeader().setStretchLastSection(True)
        
        
    def retranslateUI(self):
        if self.inverse:
            first_item = _("Table",'Name')
            second_item = _("Table",'Date')
        else:
            first_item = _("Table",'Date')
            second_item = _("Table",'Name')
        self.setHorizontalHeaderLabels([first_item,second_item,_('Table','Status'),_("Table",'Class'),_("Table",'Colour'),_("Table",'Temporal/Sanctoral'),_("Table",'Time'),_('Table','Station')])
        
        
class ItemsCreator(SuperTranslator):
    """Convenient class for printing data in both Table and Tree Widgets"""
    fontOmitted = QFont() # font used for feasts omitted
    fontOmitted.setItalic(True)
    
    
    def __init__(self,parent):
        SuperTranslator.__init__(self)
        self.parent = parent
        self.retranslateUI()
        
    
    def createLine(self,data,itemParent=None,itemLine=None):
        """Creates a line of results in Tree or in Table"""
        texts = self.presentData(data)
        if isinstance(self.parent,Tree):
            child = QTreeWidgetItem(itemParent,[texts[0],*texts[2]])
            if data.omission:
                for i in range(8):
                    child.setFont(i,self.fontOmitted)
        else:
            self.parent.setItem(itemLine,self.parent.name_pos,QTableWidgetItem(texts[0]))
            self.parent.setItem(itemLine,self.parent.date_pos,QTableWidgetItem(texts[1]))
            for i,elt in enumerate(texts[2]):
                self.parent.setItem(itemLine,i+2,QTableWidgetItem(elt))
            if data.omission:
                for column in range(self.parent.nbColumn):
                    self.parent.item(itemLine,column).setFont(self.fontOmitted)
        
    def presentData(self,data):
        """Presents the data as they will be printed on the screen"""
        name = data.nom['francais']
        date = str(data.date)
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
            status += _("ItemsCreator"," & transferred from {}".format(data.date_originelle))
        degree = self.classes[data.degre]
        colour = data.couleur.capitalize()
        temporsanct = self.tempOrSanct[data.temporal]
        time = first_upper(officia.affiche_temps_liturgique(data,'francais'))
        station = data.__dict__.get('station',{"francais":''})['francais']
        return name, date, (status, degree, colour, temporsanct, time, station)
        
    def retranslateUI(self):
        self.tempOrSanct = {True:_('ItemsCreator','Temporal'),False:_('ItemsCreator','Sanctoral')}
        self.classes = {1:_('ItemsCreator','First Class'),
                        2:_('ItemsCreator','Second Class'),
                        3:_('ItemsCreator','Third Class'),
                        4:_('ItemsCreator','Fourth Class'),
                        5:_('ItemsCreator','Commemoration'),}
       
        
    
