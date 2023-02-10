from socket import *


def main():
    server_sd = socket(AF_INET, SOCK_STREAM)
    port = 12000
    server_ip = '127.0.0.1'

    # bind the address to the socket
    server_sd.bind((server_ip, port))

    # activate listening to the socket
    server_sd.listen(1)

    # server waits for accept() for connections
    conn_sd, addr = server_sd.accept()

    # read data from the client and print it
    received_line = conn_sd.recv(1024).decode()

    print(received_line)

    # send data back over the connection
    conn_sd.send(received_line.encode())
    conn_sd.close()
    server_sd.close()


main()
