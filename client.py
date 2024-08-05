import socket
import pickle

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 39870
        self.addr = (self.server, self.port)

    def connect(self, name):
        """return id of the client that connected"""
        self.client.connect(self.addr)
        self.client.send(str.encode(name))
        val = self.client.recv(8)
        return int(val.decode())

    def send_data(self, data):
        try:
            serialized_data = pickle.dumps(data)
            self.client.sendall(serialized_data)
        except socket.error as e:
            print(e)
            pass

    def receive_data(self):
        try:
            data = self.client.recv(4096)
            if data:
                return pickle.loads(data)
        except:
            return None
        return None
