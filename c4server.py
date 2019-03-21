#Connect Four client/server program (Server portion)

import socket
import select
import sys
import datetime
import os
import string
import array

now = datetime.datetime.now(datetime.timezone.utc)
date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
HOST = "10.213.190.227" 
PORT = 4040

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#reuse address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind host IP and port to server socket
sock.bind((HOST, PORT))

sock.listen()

end = False;
conn,addr = sock.accept()
print("Connection from:", addr)

#Array Declaration with no moves made
array = [['-','-','-','-','-','-','-'], 
        ['-','-','-','-','-','-','-'], 
        ['-', '-', '-', '-','-','-','-'], 
        ['-','-','-','-','-','-','-'],
        ['-','-','-','-','-','-','-']]
#Helper function in case we need to see the server's view of the array
def printArr():
    for i in array:
        for j in i:
            print(j,end = " ")
        print('\n')

#Function that puts the current array into a string and returns the string to be sent to the client. 
def sendArr():
    ArrayString = ""

    for i in array:
        for j in i:
            ArrayString = ArrayString + " " + j
        ArrayString = ArrayString + "\n\n"

    ArrayString = ArrayString + " 0 1 2 3 4 5 6\n"
    return ArrayString

while end == False:  
    sendme = sendArr()
    sendme = sendme.encode()
    conn.sendall(sendme)

    data = conn.recv(4096).decode() #Use conn.recv for a server, not sock.recv.
    print(data)
    if data == '0':
        print("If '0' statement")
        p = 4
        while array[p][0] == 'o' or array[p][0] == 'x' and p > 0:
            p-=1
        array[p][0] = 'o'

conn.close()
 
