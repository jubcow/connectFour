import socket
import select
import sys
import re
# host (internal) IP address and port
HOST = "10.213.190.227"
PORT = 4040

#TODO Add TKinter GUI, can have buttons to send 0-6 to server and a text display for the board text.
# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST,PORT))#Initial connection being made using the IP address of the server and correct port number
except:
    print('Not connected\n')
    sys.exit()
while True:
    data = sock.recv(1024)
    data = data.decode()
    print(data)
    formatted = False
    while formatted == False:
        msg = input()
        if int(msg) > 6 or int(msg) < 0:
            print("Enter a number 0-6\n")
        else:
            formatted = True
    send = msg.encode()
    sock.sendall(send)
