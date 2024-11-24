import socket
import threading

server = "127.0.0.1"
port = 39807

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(40)  # 40 clients can be connected
print(f"[SERVER STARTED] Waiting for a connection on {server}:{port}...")

clients = []
available_ids = set(range(1, 9))  # Maximum players: 8
lock = threading.Lock()

def handle_client(conn, addr, client_id):
    print(f"New connection: {addr}")
    name = conn.recv(16).decode("utf-8")
    print(f"[LOG] {name} connected to the server.")
    conn.send(str.encode(str(client_id)))

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            for client in clients:
                if client != conn:
                    client.send(data)
        except:
            break

    with lock:
        clients.remove(conn)
        available_ids.add(client_id)  # Reclaim the ID

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected. ID {client_id} released.")

while True:
    conn, addr = s.accept()

    with lock:
        if available_ids:
            client_id = available_ids.pop()
        else:
            print("[ERROR] No available IDs. Connection refused.")
            conn.close()
            continue

        clients.append(conn)

    thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
    thread.start()
    print(f"Active connections: {threading.active_count() - 1}")
    print(f"Conn: {conn}")
    print(f"Clients: {len(clients)}")

