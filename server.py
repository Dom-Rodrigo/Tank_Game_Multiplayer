import socket
import threading
import pickle

server = "127.0.0.1"
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4) # 4 tanks can be connected
print(f"[SERVER STARTED] Waiting for a connection on {server}:{port}...")

clients = []
def handle_client(conn, addr):
    print(f"New connection: {addr}")
    while True:
        try:
            data = conn.recv(4096)
            print("received: ", pickle.loads(data))
            if not data:
                break
            for client in clients:
                if client != conn:
                    client.send(data)
        except:
            clients.remove(conn)
            conn.close()
            break

def main():
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
