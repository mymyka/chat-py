import socket
import string
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost",8080))


while True:
    user_input = input("You: ")
    client.send(user_input.encode())
    print(client.recv(1024).decode())


