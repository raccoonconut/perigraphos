#!/usr/bin/python3
import sys
import os
from subprocess import Popen, PIPE, call as call_ext
from PyQt5.QtWidgets import (QApplication,
QWidget, QFileDialog, QMainWindow,
QPushButton, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtSvg
from PyQt5.QtCore import QProcess

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


server_proc = None


class ControlWidgets(QWidget):

    def __init__(self, parent):
        super(ControlWidgets, self).__init__(parent)
        self.__controls()
        self.__layout()
        Database.parent = parent
        self.button1.clicked.connect(Database.start_server)
        self.button2.clicked.connect(Database.stop_server)
        self.button3.clicked.connect(Database.connect_client)

        self.button4.clicked.connect(Database.create_random_node)
        self.button5.clicked.connect(Database.list_all_vertices)

        self.server_proc = None

    def __controls(self):
        self.button1 = QPushButton("start")
        self.button2 = QPushButton("stop")
        self.button3 = QPushButton("connect")

        self.button4 = QPushButton("Create Node")
        self.button5 = QPushButton("Get Vert")
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

    def connect_client(self):
        try:
            Database.connect_client()
        except Error as e:
            print(e)


# static class for database communication (indradb)
class Database(object):
    proc = None
    client = None
    nodeID = 1
    dbPath = '/home/orestes/Workspace/bin/indradb/'
    parent = None

    @staticmethod
    def start_server(self):
        # Database.proc = Popen(dbPath + "indradb-server", stdout=PIPE, shell=True, stderr=PIPE)
        # Database.proc = QProcess.startDetached(Database.dbPath + "indradb-server")
        Database.proc = QProcess(Database.parent)
        Database.proc.start(Database.dbPath + "indradb-server")
        # stdout, stderr = Database.proc.communicate()
        # print(stdout, stderr)

    @staticmethod
    def stop_server(self):
        if Database.proc != None:
            try:
                # Database.proc.terminate()
                Database.proc.kill()
                Database.proc = None
                print('server stopped')

            except AttributeError as e:
                print('Unable to stop server ', e)


    @staticmethod
    def connect_client(self):
        Database.client = Client('0.0.0.0:8000', request_timeout=60, scheme='http')
        print(Database.client._session)

    # TEST METHOD
    @staticmethod
    def create_random_node(self):
        trans = Transaction()
        trans.create_vertex_from_type('person')
        Database.nodeID += 1
        print(Database.client.transaction(trans))

    @staticmethod
    def list_all_vertices(self):
        trans = Transaction()
        vertices = trans.get_vertices(VertexQuery.all("00000000-0000-0000-0000-000000000000", 10000))
        print(Database.client.transaction(trans))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
