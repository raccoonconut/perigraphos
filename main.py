#!/usr/bin/python3
import sys
import os
from PyQt5.QtWidgets import (QApplication,
QWidget, QFileDialog, QOpenGLWidget, QMainWindow,
QPushButton, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtSvg

from canvas import MyCanvas

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PGMP'
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.canvas = MyCanvas().native

        self.ctrlWidgets = ControlWidgets(self.mainWidget)

        self.mainLayout = QHBoxLayout(self.mainWidget)
        self.mainLayout.sizeConstraint = QLayout.SetDefaultConstraint
        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addLayout(self.ctrlWidgets.get_layout())

        self.initUI()

    def initUI(self):
        self.move(300, 300)
        self.resize(800, 600)
        self.setWindowTitle(self.title)
        self.setCentralWidget(self.mainWidget)
        self.setWindowIcon(QIcon(SCRIPT_DIR + os.path.sep + 'icon.png'))
        # self.mainLayout.addWidget(self.controls)
        # self.setCentralWidget(MyCanvas().native)
        # self.mainLayout.addWidget(4)

        # svgWidget = QtSvg.QSvgWidget('test.svg')
        # svgWidget.setGeometry(50,50,759,668)
        # svgWidget.show()
        # self.setGeometry(self.left, self.top, self.width, self.height)
        # self.layout().addWidget(self.canvas.native)
        # self.openFileNameDialog()


class ControlWidgets(QWidget):

    def __init__(self, parent):
        super(ControlWidgets, self).__init__(parent)
        self.__controls()
        self.__layout()

    def __controls(self):
        self.button1 = QPushButton("action1")
        self.button2 = QPushButton("action2")
        self.button3 = QPushButton("action3")

    def __layout(self):
        self.vbox = QVBoxLayout()

        # add buttons and control widgets in the container box
        self.vbox.addWidget(self.button1)
        self.vbox.addWidget(self.button2)
        self.vbox.addWidget(self.button3)

    def get_layout(self):
        return self.vbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
