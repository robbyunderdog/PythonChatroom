import socket
import select
import sys
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# checks if args are valid
if len(sys.argv) != 3:
    print("Correct Usage: script, ip, port")
    exit()
# sets ip to arg 1
ipAddress = str(sys.argv[1])
# sets port to arg 2
port = int(sys.argv[2])
# connects to server with args given
server.connect((ipAddress, port))

while True:
    sockets_list = [sys.stdin, server]

    if os.name == 'nt':
        # microsoft cringe voodoo magic cringe
        read_sockets = select.select([server], [], [], 1)[0]
        import msvcrt
        if msvcrt.kbhit():
            read_sockets.append(sys.stdin)
    else:
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], []) 

    #two types of input, one from server, other from user, checks if it was recieved or sent and does what it needs to
    for socks in read_sockets:
        # if message is from server, recieves, decodes, and prints it
        if socks == server:
            message = socks.recv(2048)
            print (message.decode())
        # else its client message, takes in, encodes, sends, and writes it
        else:
            message = sys.stdin.readline()
            server.send(message.encode())
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()