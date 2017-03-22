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
import adjutoria
import annus
import officia
os.chdir(chemin)

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QCoreApplication, QDate, QLocale, Qt, QTranslator
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QCalendarWidget, QCheckBox, QComboBox, QDateEdit, QDockWidget, QGroupBox, QHBoxLayout, QMainWindow, QLabel, QLineEdit, QPushButton, QSlider, QSpinBox, QTableWidget, QTableWidgetItem, QTabWidget, QTreeWidget, QVBoxLayout, QWidget

_ = QCoreApplication.translate # a name more convenient
current = QDate().currentDate()
calendrier = calendar.Calendar(firstweekday=6)

class ReTranslateBox():
    """A class which can contain only items with the retranslateUI function"""
    def __iter__(self):
        """Iters values of  self.__dict__"""
        for value in self.__dict__.values():
            yield value
        
    def __repr__(self):
        """Returns self.__dict__ to be recognized in the interactive interpreter"""
        return str(self.__dict__)
    
    def __setattr__(self,attribute,value):
        """Tests wether the 'value' is an object which has the function retranslateUI in it. If it is true, set the 'attribute'. This function should be useless in prod."""
        if 'retranslateUI' in value.__dir__():
            self.__dict__[attribute] = value
        else:
            raise TypeError("""Could not set attribute '{}' : '{}' object doesn't contain any 'retranslateUI' method.""".format(attribute,value))
        
class SuperTranslator():
    """A class which should be inherited by every custom widget class to make an easy translation on the fly."""
    
    def __init__(self):
        """This method only defines a ReTranslateBox object which is called 'W'. This attribute can only store widgets with a 'retranslateUI' method, i.e. from objects which inherit of this class"""
        self.W = ReTranslateBox()
        
    def retranslateUI(self):
        """This method calls every 'retranslateUI' methods of the 'W' attribute.
        This method should be overloaded by every widget which contains
        widgets to be immediately retranslated
        (i.e., which are not custom widgets).
        User shouldn't forget to call this function if necessary in the function itself :
        SuperTranslator.retranslateUI()"""
        for a in self.W:
            a.retranslateUI()
            
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
        self.execute = Main()

class Main(QMainWindow,SuperTranslator):
    """Main window"""
    def __init__(self):
        """Function which initializes the main window"""
        
        QMainWindow.__init__(self)
        SuperTranslator.__init__(self)
        self.Annee = annus.LiturgicalCalendar()
        self.actions()
        self.initUI()
        
        self.W.onglets.W.tab1.cal.clicked[QDate].connect(self.useDate)
        self.W.onglets.W.tab1.kw_bouton.clicked.connect(self.useKeyWord)
        self.W.onglets.W.tabPlus.bt_week.clicked.connect(self.useWeek)
        
    def menu(self):
        """A function which describes the menubar of the main window"""
        menubar = self.menuBar()
        
        # File menu
        self.fileMenu = menubar.addMenu('file')
        self.fileMenu.addAction(self.settingsAction)
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
        
        # Settings
        
        self.settingsAction = QAction(QIcon('icons/settings.png'),'settings',self) # icons https://www.iconfinder.com/icons/353407/cog_settings_icon#size=128
        
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
        self.tableau = QTableWidget()
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
        self.setGeometry(400,200,1500,700) # TODO centrer la fenêtre au démarrage
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
        
        self.exitAction.setText(_('Main','Exit'))
        self.exitAction.setStatusTip(_('Main','Exit the app'))
        
        self.chooseLanguageLatin.setText(_('Main','Latin'))
        self.chooseLanguageFrench.setText(_('Main','French'))
        self.chooseLanguageEnglish.setText(_('Main','English'))
        
        #initUI
        #widgets on the right
        self.rightDock.setWindowTitle(_('Main','Research'))
        
        
    def useDate(self,date):
        self.setCentralWidget(self.tableau)
        self.setWindowTitle('Theochrone - ' + date.toString())
        print(date.day(),date.month(),date.year())
        debut = fin = date.toPyDate()
        self.Annee(debut.year)
        selection = self.Annee[debut]
        self.tableau.setRowCount(len(selection))
        self.tableau.setColumnCount(5)
        for i, elt in enumerate(selection):
            self.tableau.setItem(i,0,QTableWidgetItem(elt.nom['francais']))
            self.tableau.setItem(i,1,QTableWidgetItem(str(elt.degre)))
            self.tableau.setItem(i,2,QTableWidgetItem(elt.couleur))
            self.tableau.setItem(i,3,QTableWidgetItem(officia.affiche_temps_liturgique(elt,self.Annee,'francais').capitalize()))
            if elt.temporal:
                temps = 'Temporal'
            else:
                temps = 'Sanctoral'
            self.tableau.setItem(i,4,QTableWidgetItem(temps))
            
        
        
    def useKeyWord(self):
        self.setCentralWidget(self.tableau)
        keyword = self.W.onglets.W.tab1.keyword.text()
        if keyword == '':
            return
        self.setWindowTitle('Theochrone - ' + keyword)
        annee = self.W.onglets.W.tab1.spinbox.value()
        print(annee,keyword)
        debut, fin = datetime.date(annee,1,1), datetime.date(annee, 12,31)
        self.Annee(debut.year)
        if self.W.onglets.W.tab1.plus.isChecked():
            plus = True
        else:
            plus = False
        selection = officia.inversons(keyword,self.Annee,debut,fin,exit=False,plus=plus) # plantage en cas de recherche sans résultat...
        self.tableau.setRowCount(len(selection))
        self.tableau.setColumnCount(6)
        for i, elt in enumerate(selection):
            self.tableau.setItem(i,0,QTableWidgetItem(elt.nom['francais']))
            self.tableau.setItem(i,1,QTableWidgetItem(str(elt.date)))
            self.tableau.setItem(i,2,QTableWidgetItem(str(elt.degre)))
            self.tableau.setItem(i,3,QTableWidgetItem(elt.couleur))
            self.tableau.setItem(i,4,QTableWidgetItem(officia.affiche_temps_liturgique(elt,self.Annee,'francais').capitalize()))
            if elt.temporal:
                temps = 'Temporal'
            else:
                temps = 'Sanctoral'
            self.tableau.setItem(i,5,QTableWidgetItem(temps))
            
    def useWeek(self):
        self.setCentralWidget(self.arbre)
        tab=self.W.onglets.W.tabPlus
        year = tab.wy_spinbox.text()
        month = tab.monthweek_combo.currentIndex() + 1
        week = tab.week_combo.currentIndex()
        self.Annee(year)
        WEEK = self.Annee.weekmonth(year,month,week)
        self.arbre.setColumnCount(1)
        self.arbre.
        
        
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
                
class Tree(QWidget,SuperTranslator):
    """A class which defines the main widget used with multiple days"""
    def __init__(self,debut,fin,data):
        QWidget.__init__(self)
        SuperTranslator.__init__(self)
        self.initUI(debut,fin)
        
    def initUI(self): 
        self.arbre = QTreeWidget()
        self.arbre.setHeaderHidden(True)
        depth = lambda L: isinstance(L, list) and max(map(depth, L),default=0)+1 #http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to
        
        
    
