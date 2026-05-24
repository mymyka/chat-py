import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.13",8080))


while True:
    user_input = input("You: ")
    client.send(user_input.encode())
    print(client.recv(1024).encode)


