#!/usr/bin/python3
import sys
import os
from subprocess import Popen, PIPE
from PyQt5.QtWidgets import (QApplication,
QWidget, QFileDialog, QMainWindow,
QPushButton, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtSvg

from canvas import MyCanvas
from indradb import *

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PGMP'
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.canvas = MyCanvas(10000).native

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


path = '/home/orestes/Workspace/bin/indradb/'
server_proc = None


class ControlWidgets(QWidget):

    def __init__(self, parent):
        super(ControlWidgets, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.button1.clicked.connect(self.call_indradb)
        self.button2.clicked.connect(Database.stop_server)
        self.button3.clicked.connect(Database.connect_client)

        self.server_proc = None

    def __controls(self):
        self.button1 = QPushButton("start")
        self.button2 = QPushButton("stop")
        self.button3 = QPushButton("connect")

        self.button4 = QPushButton("MaxPaths")
        self.button5 = QPushButton("Generate")
        self.button6 = QPushButton("connect")


    def __layout(self):
        self.vbox = QVBoxLayout()

        # add buttons and control widgets in the container box
        self.vbox.addWidget(self.button1)
        self.vbox.addWidget(self.button2)
        self.vbox.addWidget(self.button3)
        self.vbox.addWidget(self.button4)
        self.vbox.addWidget(self.button5)
        self.vbox.addWidget(self.button6)


    def get_layout(self):
        return self.vbox

    def call_indradb(self):
        Database.start_server(path)
        print('hello')

    def connect_client(self):
        try:
            Database.connect_client()
        except Error as e:
            print(e)


# static class for database communication (indradb)
class Database(object):
    proc = None
    client = None

    @staticmethod
    def start_server(dbPath):
        Database.proc = Popen(['exec', dbPath + "indradb-server"], stdout=PIPE, shell=True, stderr=PIPE)

    @staticmethod
    def stop_server(self):
        try:
            Database.proc.terminate()
            print(PIPE)
        except AttributeError as e:
            print(e)

    @staticmethod
    def connect_client(self):
        Database.client = Client('0.0.0.0:8000', request_timeout=60, scheme='https')
        print(Database.client.scheme)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
