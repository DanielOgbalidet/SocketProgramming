import socket
import threading
from socket import *
import _thread as thread
import time

# making lists for clients connected to server and names. Also making lists and variables for use when playing the game
clients = []
PlayWaiting = 0
players = []
names = ["TurboSlayer", "CrypticHatter", "CrashTV", "Masked Titen", "Venom Fate"]


# function for time of connection
def now():
    # returns the time of day
    return time.ctime(time.time())


# function for handling the clients connected to the server
def handle_client(connection):
    global PlayWaiting
    # appointing random names for each client
    name = names[clients.index(connection)]
    # Welcoming messages for when a client log in
    connection.send("Write 'play' to play a game".encode())
    connection.send("\nTo send a message to other players, write whatever you like and hit 'enter'".encode())
    connection.send(("\nYou will be given a random username. Your username is " + name).encode())
    # loop that will either send a message to the rest of the clients or start a game
    while True:
        data = connection.recv(1024).decode()
        print("received  message = ", data)
        # if 'play' is written, an invitation will be sent to all the other clients
        if data == "play":
            players_add(connection)
            for client in clients:
                if connection != client:
                    message = "You have an invite for a game from " + name + ". Do you accept?(yes/no)"
                    client.send(message.encode())
                    PlayWaiting = PlayWaiting + 1
                    print(PlayWaiting)
            break
        # if an invitation is sent and you write 'yes', a new game will start
        if data == "yes" and PlayWaiting > 0:
            players_add(connection)
            PlayWaiting = 0
            x = threading.Thread(target=play_game, args=(players[0], players[1]))
            x.start()
            for client in clients:
                if client != players[0] and client != players[1]:
                    # if someone accepts, the other ones will be notified of that
                    client.send("Sorry, another player accepted the game".encode())
            break
        else:
            # if play isn't written, the message will be broadcast to all the other clients
            broadcast_all(data, connection)
    # connection.close()


# adds player to the player array. Is used when starting a game
def players_add(player):
    players.append(player)


# starts a game between two clients
def play_game(connection1, connection2):
    global players
    connection1.send("Rules: Type exit on your turn to exit the game and wait for your turn to choose".encode())
    connection2.send("Rules: Type exit on your turn to exit the game and wait for your turn to choose".encode())

    # game will continue until someone exits the game
    while True:
        connection1.send("Your turn, choose 'rock', 'paper' or 'scissors'".encode())
        connection2.send("Waiting for other player...".encode())
        choice1 = connection1.recv(1024).decode()
        # if one of the players writes 'exit', they both get sent back to handle_client()
        if choice1 == "exit":
            thread.start_new_thread(handle_client, (connection1,))
            connection2.send("Other player left the game".encode())
            thread.start_new_thread(handle_client, (connection2,))
            break
        connection2.send("Your turn, choose 'rock', 'paper' or 'scissors'".encode())
        connection1.send("Waiting for other player...".encode())
        choice2 = connection2.recv(1024).decode()
        if choice2 == "exit":
            thread.start_new_thread(handle_client, (connection2,))
            connection1.send("Other player left the game".encode())
            thread.start_new_thread(handle_client, (connection1,))
            break
        # if and else tests for the rock, paper, scissors game
        if choice1 == "rock" and choice2 == "scissors":
            winner = connection1
            loser = connection2
        elif choice1 == "scissors" and choice2 == "paper":
            winner = connection1
            loser = connection2
        elif choice1 == "paper" and choice2 == "rock":
            winner = connection1
            loser = connection2
        elif choice2 == "rock" and choice1 == "scissors":
            winner = connection2
            loser = connection1
        elif choice2 == "scissors" and choice1 == "paper":
            winner = connection2
            loser = connection1
        elif choice2 == "paper" and choice1 == "rock":
            winner = connection2
            loser = connection1
        else:
            winner = None
            loser = None
        if winner:
            winner.send("You win!".encode())
            loser.send("You lose!".encode())
        elif choice1 == choice2:
            connection1.send("Draw!".encode())
            connection2.send("Draw!".encode())
        else:
            connection1.send("Invalid choice was used by one of the players".encode())
            connection2.send("Invalid choice was used by one of the players".encode())


# Notifies all the clients when a new client joins
def broadcast(client_list):
    message = "New player has joined"
    for client in client_list:
        client.send(message.encode())


# function to broadcast message to all the other clients
def broadcast_all(data, connection):
    index = clients.index(connection)
    for client in clients:
        if connection != client:
            name = names[index]
            message = data + " from " + name
            client.send(message.encode())


# function to connect with clients
def main():
    # creates a server socket, listens for new connections, and spawns a new thread whenever a new connection join
    server_port = 12000
    server_socket = socket(AF_INET, SOCK_STREAM)

    try:
        # Binds with ip address and port
        server_socket.bind(('127.0.0.2', server_port))
        # Print in case of error
    except:
        print("Bind failed. Error : ")

    # can connect to 128 different clients
    server_socket.listen(128)
    print('The server is ready to receive')

    # Connects to client, broadcasts to all the other clients and sends them to the handle_client function
    while True:
        connection_socket, addr = server_socket.accept()
        broadcast(clients)
        # adds client to the client list
        clients.append(connection_socket)
        print('Server connected by ', addr)
        print('at ', now())
        # starts a new thread with the handle_client function
        thread.start_new_thread(handle_client, (connection_socket, ))

    # serverSocket.close()


if __name__ == '__main__':
    main()
