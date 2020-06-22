import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

import qml
import images

if __name__ == "__main__":
	app = QApplication(sys.argv)
	engine = QQmlApplicationEngine()
	engine.quit.connect(app.quit)
	engine.load("qml/main.qml")
	sys.exit(app.exec_())
