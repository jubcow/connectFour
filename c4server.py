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

#Function for AI taking a turn, currently just random, but will want to implement an algorithm to make smarter
def aiTurn():
    r = 5
    c = random.randrange(6)
    while array[r][c] == 'o' or array[r][c] == 'x' and r > 0: 
        r-=1
    array[r][c] = 'x'

end = False
#Will check the board to see if the player or AI has connected 4
def checkEnd():
    r = 6
    c = 7
    for i in range(r):
        for j in range(c):
            print("Array i's: "+ str(i) +" "+ array[i][j] + array[i-1][j] + array[i-2][j] + array[i-3][j])
            print("Array j's: "+ str(j) +" "+ array[i][j] + array[i][j-1] + array[i][j-2] + array[i][j-3]) 
            #print(array[i][j], end='')
            if i > 2:
                if array[i][j] == 'o' and array[i-1][j] == 'o'  and array[i-2][j] == 'o' and array[i-3][j] == 'o': #if they have a vertical connect4
                    sendme = sendArr() + "You win! (Vert)\n"
                    sendme = sendme.encode()
                    conn.sendall(sendme)
                    quit()
            if j > 2:    
                if array[i][j] == 'o' and array[i][j-1] == 'o'  and array[i][j-2] == 'o' and array[i][j-3] == 'o': #horizontal win, the if statement is to avoid a wrapping bug in which one could win with something like 4 5 6 0. 
                    sendme = sendArr() + "You win! (Horiz)\n"
                    sendme = sendme.encode()
                    conn.sendall(sendme)
                    quit()
            elif array[i][j] == 'o' and array[i-1][j-1] == 'o' and array[i-2][j-2] == 'o' and array[i-3][j-3] == 'o':
                sendme = sendArr() + "You win! (Diag: \)\n"
                sendme = sendme.encode()
                conn.sendall(sendme)
                quit()
            elif j < 6:
                if array[i][j] == 'o' and array[i-1][j+1] == 'o' and array[i-2][j+2] == 'o' and array[i-3][j+3] == 'o':
                    sendme = sendArr() + "You win! (Diag: /)\n"
                    sendme = sendme.encode()
                    conn.sendall(sendme)
                    quit()

            if i > 2:        
                if array[i][j] == 'x' and array[i-1][j] == 'x'  and array[i-2][j] == 'x' and array[i-3][j] == 'x': #if they have a vertical connect4
                    sendme = sendArr() + "You lose. (Vert)\n"
                    sendme = sendme.encode()
                    conn.sendall(sendme)
                    quit()
            elif j > 2:
                if array[i][j] == 'x' and array[i][j-1] == 'x'  and array[i][j-2] == 'x' and array[i][j-3] == 'x': #horizontal win, the if statement is to avoid a wrapping bug in which one could win with something like 4 5 6 0.
                    sendme = sendArr() + "You lose. (Horiz)\n"
                    sendme = sendme.encode()
                    conn.sendall(sendme)
                    quit()
            elif array[i][j] == 'x' and array[i-1][j-1] == 'x' and array[i-2][j-2] == 'x' and array[i-3][j-3] == 'x':
                sendme = sendArr() + "You lose. (Diag: \)\n"
                sendme = sendme.encode()
                conn.sendall(sendme)
                quit()
            elif j < 6:
                if array[i][j] == 'x' and array[i-1][j+1] == 'x' and array[i-2][j+2] == 'x' and array[i-3][j+3] == 'x':
                    sendme = sendArr() + "You lose. (Diag: /)\n"
                    sendme = sendme.encode()
                    conn.sendall(sendme)
                    quit()


while end == False:  
    checkEnd() #Check if the player has won

    sendme = sendArr()
    sendme = sendme.encode()
    conn.sendall(sendme)

    data = conn.recv(4096).decode() #Use conn.recv for a server, not sock.recv.
    print(data)
    r = 5
    c = int(data)
    while array[r][c] == 'o' or array[r][c] == 'x' and r > 0: # 'x' represents the AI, 'o' is player
        r-=1
    array[r][c] = 'o'

    #checkEnd() #Check to see if player has won
    aiTurn() #AI takes turn afterwards

conn.close()
 
