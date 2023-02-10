from socket import *
import sys
import threading

# Making a socket to connect with server
serverName = '127.0.0.2'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
# trying to connect
try:
    clientSocket.connect((serverName, serverPort))
except:
    print("ConnectionError")
    sys.exit()


# function for sending messages to server
def send():
    while True:
        data = input()
        clientSocket.send(data.encode())


# function for receiving messages from server
def receive():
    while True:
        print(clientSocket.recv(1024).decode())


# making thread so that client can receive and send messages simultaneously
if __name__ == "__main__":
    x = threading.Thread(target=send, args=())
    y = threading.Thread(target=receive, args=())
    x.start()
    y.start()
