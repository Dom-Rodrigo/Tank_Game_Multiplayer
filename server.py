import socket
import threading
import pickle

server = "127.0.0.1"
port = 39807

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(40) # 40 tanks can be connected
print(f"[SERVER STARTED] Waiting for a connection on {server}:{port}...")

clients = []
id = 0
def handle_client(conn, addr, id):

    print(f"New connection: {addr}")
    name = conn.recv(16).decode("utf-8")
    print(f"[LOG] {name} connected to the server.")
    conn.send(str.encode(str(id)))
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                clients.remove(conn)
                conn.close()
            for client in clients:
                if client != conn:
                    client.send(data)
        except:
            if conn in clients:
                clients.remove(conn)
            conn.close()
            break

while True:
    conn, addr = s.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr, id))
    thread.start()
    print(f"Active connections: {threading.active_count() - 1}")
    print(f"Conn : {conn}")
    print(f"Clients: {clients}")
    id += 1
