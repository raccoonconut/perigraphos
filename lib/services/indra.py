from indradb import *
from PyQt5.QtCore import QProcess


# static class for database communication (indradb)
class Database(object):
    proc = None
    client = None
    nodeID = '00000000-0000-0000-0000-000000000000'
    dbPath = '/home/orestes/Workspace/bin/indradb/'
    parent = None

    @staticmethod
    def start_server(self):
        Database.proc = QProcess(Database.parent)
        Database.proc.start(Database.dbPath + "indradb-server")
        # Wait for server to start and then connect
        if Database.proc.waitForStarted(msecs=3000):
            Database.client = Client('0.0.0.0:8000', request_timeout=60, scheme='http')
            print("Database Connected")

    @staticmethod
    def stop_server(self):
        if Database.proc is not None:
            try:
                Database.proc.terminate()
                Database.proc = None
                print('Server stopped')
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
        vertices = trans.get_vertices(VertexQuery.all(None, 10000))
        print(vertices)
        print([x.type for x in Database.client.transaction(trans)[0]])
