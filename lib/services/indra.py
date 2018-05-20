from indradb import *
from PyQt5.QtCore import QProcess
import random

# static class for database communication (indradb)
class Database(object):
    proc = None
    client = None
    nodesID = '00000000-0000-0000-0000-000000000000'
    dbPath = '/home/orestes/Workspace/bin/indradb/'
    parent = None
    adj = None

    @staticmethod
    def start_server(self):
        Database.proc = QProcess(Database.parent)
        Database.proc.start(Database.dbPath + "indradb-server")
        # Wait for server to start and then connect
        if Database.proc.waitForStarted(msecs=3000):
            Database.client = Client('0.0.0.0:8000', request_timeout=60, scheme='http')
            print("Database Connected")

    def stop_server():
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

    def create_random_dataset(self):
        trans = Transaction()
        for i in range(100):
            trans.create_vertex_from_type('person')
        vertices = Database.client.transaction(trans)

        Database.client.transaction(trans)

        ed = Database.make_edges(vertices, 20)
        ed = list(ed)

        ek = EdgeKey(ed[0][0], 'relation', ed[0][1])
        trans = Transaction()
        print('the key of this edge is: {}'.format(ek.to_dict()))
        Database.edk = trans.create_edge(EdgeKey(ed[0][0], 'relation', ed[0][1]))
        Database.client.transaction(trans)
        # print(tuple(edges))

    def make_edges(lst, max_iter):
        ed = ([],[])
        i = 0
        temp_lst = lst[:]

        for j in range(2):
            while len(temp_lst) > 0:
                idx = random.randrange(0, len(temp_lst))
                i += 1
                if random.getrandbits(1):
                    ed[j].append(temp_lst.pop(idx))
                else:
                    ed[j].append(temp_lst[idx])
                if i == max_iter:
                    break

        return zip(ed[0],ed[1])

    @staticmethod
    def list_all_vertices(self):
        trans = Transaction()
        vertices = trans.get_vertices(VertexQuery.all(None, 10000))

        Database.nodesID = tuple(x.id for x in Database.client.transaction(trans)[0])
        # return Database.nodesID
        print(Database.nodesID)

    def list_all_edges():
        trans = Transaction()
        ed = trans.get_edges(VertexQuery.all(None, 1000))

        print([x.id for x in Database.client.transaction(trans)])
