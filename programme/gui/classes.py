#!/usr/bin/python3
# -*-coding:Utf-8 -*

import datetime
import os.path
import sys

gui = os.path.dirname(os.path.abspath(__file__))
theo = gui + '/..'
os.chdir(theo)
sys.path.append(theo)
import adjutoria
import officia 

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QCoreApplication, QDate, QLocale, Qt, QTranslator
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QCalendarWidget, QCheckBox, QComboBox, QDockWidget, QHBoxLayout, QMainWindow, QLabel, QLineEdit, QPushButton, QSlider, QSpinBox, QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget

_ = QCoreApplication.translate # a name more convenient

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
        os.chdir(gui)
        QMainWindow.__init__(self)
        SuperTranslator.__init__(self)
        self.Annee = {}
        self.actions()
        self.initUI()
        
        self.W.onglets.W.tab1.cal.clicked[QDate].connect(self.useDate)
        self.W.onglets.W.tab1.kw_bouton.clicked.connect(self.useKeyWord)
        
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
        self.setCentralWidget(self.tableau)
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
        self.setGeometry(400,400,1000,1000) # TODO centrer la fenêtre au démarrage
        current = QDate()
        os.chdir(theo)
        current = current.currentDate()
        self.W.onglets.W.tab1.spinbox.setValue(current.year())
        self.useDate(current)
        self.retranslateUI() # voir si on ne la met pas carrément dans l'app, qui hériterait elle aussi de SuperTranslator
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
        self.setWindowTitle('Theochrone - ' + date.toString())
        print(date.day(),date.month(),date.year())
        debut = fin = date.toPyDate()
        if debut not in self.Annee:
            self.Annee.update(officia.fabrique_an(debut,fin))
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
        keyword = self.W.onglets.W.tab1.keyword.text()
        if keyword == '':
            return
        self.setWindowTitle('Theochrone - ' + keyword)
        annee = self.W.onglets.W.tab1.spinbox.value()
        print(annee,keyword)
        debut, fin = datetime.date(annee,1,1), datetime.date(annee, 12,31)
        if debut not in self.Annee:
            self.Annee.update(officia.fabrique_an(debut,fin))
        if self.W.onglets.W.tab1.plus.isChecked():
            plus = True
        else:
            plus = False
        selection = officia.inversons(keyword,self.Annee,debut,fin,plus=plus)
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
        self.tabPlus = QWidget()
        
        self.tabs.addTab(self.W.tab1,"1")
        self.tabs.addTab(self.tabPlus,"+")
        
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

        self.layout = QVBoxLayout()
        
        self.cal_label = QLabel('cal_label',self)
        self.layout.addWidget(self.cal_label)
        
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setFirstDayOfWeek(0)
        self.cal.setMinimumDate(QDate(1600,1,1))
        self.cal.setMaximumDate(QDate(4100,12,31))

        self.layout.addWidget(self.cal)
        self.layout.addStretch(1)
        
        self.slider_layout = QHBoxLayout()
        
        self.kw_label = QLabel('kw_label',self)
        self.layout.addWidget(self.kw_label)
        
        self.keyword = QLineEdit(self)
        self.layout.addWidget(self.keyword)
        
        self.plus = QCheckBox('More results',self)
        self.layout.addWidget(self.plus)
        
        self.spinbox = QSpinBox()
        self.spinbox.setMaximum(4100)
        self.spinbox.setMinimum(1600)
        
        self.kw_bouton = QPushButton('kw_button',self)
        
        self.slider_layout.addWidget(self.spinbox)
        self.slider_layout.addWidget(self.kw_bouton)
        
        self.layout.addLayout(self.slider_layout)        
        self.layout.addStretch(2)
        
        self.setLayout(self.layout)
        
    def retranslateUI(self):
        SuperTranslator.retranslateUI(self)
        
        self.cal_label.setText(_('Unique','Please select a date : '))
        self.kw_label.setText(_('Unique',"Please enter keywords : "))
        self.plus.setText(_('Unique','More results'))
        self.kw_bouton.setText(_('Unique','OK'))
        
        self.cal.setLocale(QLocale()) # à mettre dans la toute première fonction
        
        
        
        
    
