import socket
import threading

HEADER = 64
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ["N", "n"]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        data = []
        conn.send("Input your name: ".encode(FORMAT))
        data.append(receiveData(conn, addr))
        conn.send("Input your body height (cm): ".encode(FORMAT))
        data.append(receiveData(conn, addr))
        conn.send("Input your body weight: ".encode(FORMAT))
        data.append(receiveData(conn, addr))

        result = calculateBMI(data)
        if (result >= 18.5 and result < 25):
            desc = "You have normal weight"
        elif (result >= 25 and result < 30):
            desc = "You are overweight, do exercise more and be healthy!"
        elif (result >= 30 and result < 40):
            desc = "You have obesity, consult to a doctor"
        elif (result >= 40):
            desc = "You have morbit obesity. Good lord go to a doctor now if you haven't already!"
        else:
            desc = "Too light(?) Outside of BMI measurement"
        
        conn.send(f"{data[0]}, your Body Mass Index is: {str(result)}. \nDescription: {desc}\n\nCalculate again? Y/N".encode(FORMAT))

        confirm_msg = receiveData(conn, addr)
        if (confirm_msg in DISCONNECT_MESSAGE):
            connected = False
            print(f"[{addr}] Client disconnected.")

    conn.close()

def receiveData(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        print(f"[{addr}] {msg}")

        return msg

def calculateBMI(data):
    calculation = int(data[2]) / ((int(data[1])/100)**2)
    print(calculation)
    return calculation

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")

print(f"[STARTING] server is starting...")
start()