import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",9999))


while True:
    user_input = input("You: ")
    client.send(user_input.encode())
    print(client.recv(1024))


