import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))

server.listen(5)

state = {}

while True:
    client, addr = server.accept()
    state[addr] = client