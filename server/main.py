import socket
import threading
from typing import Dict, Any, List

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 8080))
server.listen(5)

state: Dict[Any, socket.socket] = {}
is_stopping = threading.Event()
threads: List[threading.Thread] = []

def broadcast(message: str, sender_addr: Any):
    for addr, client_socket in state.items():
        if addr != sender_addr:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"Error sending to {addr}: {e}")

def handle_client(client_socket: socket.socket, addr: Any):
    client_socket.settimeout(1.0)
    while not is_stopping.is_set():
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"Received from {addr}: {message}")
            broadcast(message, addr)
        except socket.timeout:
            continue

def main():
    server.settimeout(1.0)
    while not is_stopping.is_set():
        try:
            client_socket, addr = server.accept()
            state[addr] = client_socket
            t = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
            threads.append(t)
            t.start()
        except socket.timeout:
            continue

    for t in threads:
        t.join()

server_thread = threading.Thread(target=main, daemon=True)
server_thread.start()

input("Press Enter to stop the server...\n")

is_stopping.set()
server_thread.join()
server.close()