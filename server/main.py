import socket
import threading
from typing import Any, Dict

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)

state: Dict[Any, socket.socket] = {}
stop_event = threading.Event()

def broadcast(message: bytes, sender_addr):
    """Send message to all clients except sender."""
    for addr, client in list(state.items()):
        if addr != sender_addr:
            try:
                client.send(message)
            except Exception:
                del state[addr]  # remove dead client

def handle_client(client: socket.socket, addr):
    """Each client gets its own thread to receive messages."""
    client.settimeout(1.0)
    while not stop_event.is_set():
        try:
            message = client.recv(1024)
            if not message:
                break  # client disconnected
            broadcast(message, addr)
        except socket.timeout:
            continue
        except Exception:
            break

    client.close()
    state.pop(addr, None)
    print(f"{addr} disconnected")

def state_manager():
    """Accept new connections and spawn a thread per client."""
    server.settimeout(1.0)
    while not stop_event.is_set():
        try:
            client, addr = server.accept()
            print(f"{addr} connected")
            state[addr] = client

            # Each client needs its own receive thread
            t = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
            t.start()
        except socket.timeout:
            continue

state_thread = threading.Thread(target=state_manager, daemon=True)
state_thread.start()

input('Press Enter to stop...\n')

stop_event.set()
state_thread.join()
server.close()
print("Server stopped")