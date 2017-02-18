#!/usr/bin/python3
# -*-coding:Utf-8 -*

import messages
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QComboBox, QDockWidget, QHBoxLayout, QMainWindow, QLabel, QTableWidget, QTabWidget, QWidget

class Main(QMainWindow):
    """Main window"""
    def __init__(self):
        """Function which initializes the main window"""
        super().__init__()
        self.actions()
        self.initUI()
        
    def menu(self):
        """A function which describes the menubar of the main window"""
        _ = messages.main_window['menus']
        menubar = self.menuBar()
        
        # File menu
        fileMenu = menubar.addMenu(_['file'])
        fileMenu.addAction(self.exitAction)
        
        # Edit menu
        editMenu = menubar.addMenu(_['edit'])
        
        # Help menu
        helpMenu = menubar.addMenu(_['help'])
        
    def actions(self):
        """A function which defines actions in the main window"""
        _ = messages.main_window['actions']
        # Exit
        self.exitAction = QAction(QIcon('icons/exit.png'),_['exit_name'],self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip(_['exit_status'])
        self.exitAction.triggered.connect(self.close)
        
    def initUI(self):
        """A function which defines widgets and main features of the window"""
        _ = messages.main_window['init']
        # widgets
        # main widget
        tableau = QTableWidget()
        self.setCentralWidget(tableau)
        # widgets on the right
        self.rightDock = QDockWidget(_['right_dock'],self)
        self.rightDock.setWidget(Onglets())
        self.addDockWidget(Qt.RightDockWidgetArea,self.rightDock)
        
        # menu
        self.menu()        
        
        # statusbar
        self.statusBar()
        
        # main features
        self.setGeometry(400,400,700,600) # TODO centrer la fenêtre au démarrage
        self.setWindowTitle('Theochrone - ')
        self.show()
        
class Onglets(QWidget):
    """A class for a tab widget"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # main widgets
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tabPlus = QWidget()
        
        self.tabs.addTab(self.tab1,"1")
        self.tabs.addTab(self.tabPlus,"+")
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
class Unique(QWidget):
    """A class wich defines a widget with two types of research : for one date and for key-words."""
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        pass
        
    
