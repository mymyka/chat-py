import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))

server.listen(5)

state = {}

def state_manager():
    while True:
        client, addr = server.accept()
        state[addr] = client