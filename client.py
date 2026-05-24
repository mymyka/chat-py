import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.13",8080))


# while True:
#     user_input = input("You: ")
#     client.send(user_input.encode())
#     print("##:: " + client.recv(1024).decode())


def receving():
    while True:
        try:
            msg =  client.recv(1024).decode()
            if not msg:
                continue
            if msg:
                print(f"##:",msg)
        except:
            break

def main():
    user_input = input("You: ")
    client.send(user_input.encode())


threading.Thread(target=receving, daemon=True).start()
main()
