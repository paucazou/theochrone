#!/usr/bin/python3
# -*-coding:Utf-8 -*

import messages
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QComboBox, QDockWidget, QHBoxLayout, QMainWindow, QLabel, QTableWidget

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
        
        # widgets
        # main widget
        tableau = QTableWidget()
        self.setCentralWidget(tableau)
        # widgets on the right
        
        # menu
        self.menu()        
        
        # statusbar
        self.statusBar()
        
        # main features
        self.setGeometry(400,400,700,600) # TODO centrer la fenêtre au démarrage
        self.setWindowTitle('Theochrone - ')
        self.show()
    
