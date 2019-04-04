import socket
import select
import sys
import re
import json

a = ""
with open('addresses.json') as server_json:
    a = json.load(server_json)
    print(a)

# host (external) IP address and port
HOST = a["SERVER"]["EXTERNAL"]
PORT = int(a["SERVER"]["PORT"])

#TODO Add TKinter GUI, can have buttons to send 0-6 to server and a text display for the board text.
# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST,PORT))#Initial connection being made using the IP address of the server and correct port number
    print("connected to ",HOST,":",PORT)
except:
    print('Not connected\n')
    sys.exit()
while True:
    data = sock.recv(1024)
    data = data.decode()
    print(data)
    formatted = False
    while formatted == False:
        msg = input("Enter a number 0-6\n")
        if not (int(msg) > 6 or int(msg) < 0):
            formatted = True
            
    send = msg.encode()
    sock.sendall(send)
