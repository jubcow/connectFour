#Connect Four client/server program (Server portion)

import socket
import select
import sys
import datetime
import os
import string

now = datetime.datetime.now(datetime.timezone.utc)
date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
HOST = "10.213.190.227" #My google cloud VM
PORT = 4040

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#reuse address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind host IP and port to server socket
sock.bind((HOST, PORT))

sock.listen()

conn,addr = sock.accept()
print("Connection from:", addr)

data = conn.recv(4096).decode() #Use conn.recv for a server, not sock.recv. 
#print(data)
        
sendme = "test data"
sendme = sendme.encode()
conn.sendall(sendme)
conn.close()

        