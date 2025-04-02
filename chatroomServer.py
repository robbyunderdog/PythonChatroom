import time
import socket
import select
import sys
from _thread import *

# stores all messages in text file for safekeeping
txtFile = "chatroomMessages.txt"

# first arg AF_INET is the address domain of the socket. This is for Internet Domain with any two hosts. Second is type of socket, SOCK_STREAM means that data or characters are read continuosly
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks if args are suffiecient to try to connect
if len(sys.argv) != 3:
    print("Correct Usage: script, IP address, port")
    exit()

# takes first arg for ip
ipAddress = str(sys.argv[1])
# takes second arg for port
port = int(sys.argv[2])

# binds the server to entered ip and port, client must be aware of these
server.bind((ipAddress, port))

# listens for 100 active connections
server.listen(100)

#list of clients currently connected to server
clientList = []

def clientthread(conn, addr):
    welcomeMessage = "Welcome to chat server!"
    conn.send(welcomeMessage.encode())
    while True:
        try:
            message = conn.recv(2048)
            if message.decode():
                # prints message and address of user who sent message
                print("<" + addr[0] + "> " + message.decode())

                messageToSend = "<" + addr[0] + "> " + message.decode()
                # sends message to all clients
                broadcast(messageToSend, conn)
                # stores message in file
                with open(txtFile, "a") as file:
                    file.write(time.strftime("%m/%d/%Y %H:%M:%S") + " - " + messageToSend + "\n")
            else:
                # removes connection if no input
                remove(conn)
        except:
            continue

# broadcast the message to every client in the list
def broadcast(message, connection):
    for clients in clientList:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

# function to remove object from list
def remove(connection):
    if connection in clientList:
        clientList.remove(connection)

while True:
    # accepts the connection request and stores socket object and addr
    conn, addr = server.accept()

    clientList.append(conn)

    print(addr[0] + " connected")

    #creates a new thread for every connection
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()