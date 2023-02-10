from socket import *


def main():
    message = "Daniel"
    client_sd = socket(AF_INET, SOCK_STREAM)
    server_ip = '127.0.0.1'
    port = 12000

    # connect to the server
    client_sd.connect((server_ip, port))

    # send data
    client_sd.send(message.encode())

    # Read data from socket
    received_line = client_sd.recv(1024).decode()
    print(received_line)
    client_sd.close()


main()


