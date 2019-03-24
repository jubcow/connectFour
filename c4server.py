#Connect Four client/server program (Server portion)

import socket
import select
import sys
import datetime
import os
import string
import array
import random

#now = datetime.datetime.now(datetime.timezone.utc)
#date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
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
        ['-','-','-','-','-','-','-'], 
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
    if end == True:
        ArrayString = ArrayString + "Game End\n"
    return ArrayString

#Function for AI taking a turn, currently just random, but will want to implement an algorithm to make smarter
def aiTurn():
    r = 4
    c = random.randrange(6)
    while array[r][c] == 'o' or array[r][c] == 'x' and r > 0: 
        r-=1
    array[r][c] = 'x'

end = False
#Will check the board to see if the player or AI has connected 4
def checkEnd():
    r = 5
    c = 7
    for i in range(r):
        for j in range(c):
            #print("Array i's: " + array[i][j] + array[i-1][j] + array[i-2][j] + array[i-3][j])
            print("Array j's: " + array[i][j] + array[i][j-1] + array[i][j-2] + array[i][j-3]) 
            #print(array[i][j], end='')
            if array[i][j] == 'o' and array[i-1][j] == 'o'  and array[i-2][j] == 'o' and array[i-3][j] == 'o': #if they have a vertical connect4
                sendme = sendArr()
                sendme = sendme.encode()
                conn.sendall(sendme)
                end = True
                quit()
            elif array[i][j] == 'o' and array[i][j-1] == 'o'  and array[i][j-2] == 'o' and array[i][j-3] == 'o': #horizontal connect4 
                sendme = sendArr()
                sendme = sendme.encode()
                conn.sendall(sendme)
                end = True
                quit()
            #TODO: implement diagonals

while end == False:  
    checkEnd() #Check if the player has won

    sendme = sendArr()
    sendme = sendme.encode()
    conn.sendall(sendme)

    data = conn.recv(4096).decode() #Use conn.recv for a server, not sock.recv.
    print(data)
    r = 4
    c = int(data)
    while array[r][c] == 'o' or array[r][c] == 'x' and r > 0: # 'x' represents the AI, 'o' is player
        r-=1
    array[r][c] = 'o'

    #checkEnd() #Check to see if player has won
    aiTurn() #AI takes turn afterwards

conn.close()
 
