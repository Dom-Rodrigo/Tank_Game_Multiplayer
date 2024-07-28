import socket
import pickle

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 12345
        self.addr = (self.server, self.port)

    def connect(self):
        self.client.connect(self.addr)

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
