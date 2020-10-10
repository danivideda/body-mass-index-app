import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ["N", "n"]
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def main():
    print("============== Body Mass Index calculator App =============\n")
    connected = True
    while connected:
        print(client.recv(2048).decode(FORMAT))

        msg = input()
        send(msg)
        if (msg in DISCONNECT_MESSAGE):
            connected = False

main()