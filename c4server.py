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
HOST = "10.142.0.2" 
PORT = 4040

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#reuse address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind host IP and port to server socket
sock.bind((HOST, PORT))

def main():
    while True:
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


        end = False
        while end == False:

            # get player input / turn
            data = recString(conn) #Use conn.recv for a server, not sock.recv.
            print(data)
            r = 5
            c = int(data)
            while array[r][c] == 'o' or array[r][c] == 'x' and r > 0: # 'x' represents the AI, 'o' is player
                r-=1
            array[r][c] = 'o'

            #checks
            endRes = checkEnd('o', 'You Win!') #Check if the player has won
            if endRes[0] == 0: # previous check was code=0 'CONTINUE'
                endRes = checkDraw() # check for draw
            if endRes[0] == 1: # previous check was code=1 'END STATE'
                sendString(conn, endRes[1]) # endRes[1] contains message to send
                end == True

            if endRes[0] == 0: # previous check was code=0 'CONTINUE'
                sendme = sendArr() # send current board
                sendString(conn, sendme)

            #AI takes turn after player
            aiTurn()

            # checks
            endRes = checkEnd('x', 'You lose.') #Check if the AI has won
            if endRes[0] == 0: # previous check was code=0 'CONTINUE'
                endRes = checkDraw() # check for draw
            if endRes[0] == 1: # previous check was code=1 'END STATE'
                sendString(conn, endRes[1]) # endRes[1] contains message to send
                end == True

            if endRes[0] == 0: # if any of the above returned code=1 'END STATE'
                sendme = sendArr() # send current board
                sendString(conn, sendme)                

        conn.close()

"""
Helpful wrappers for the socket sending and recieving.
"""
def sendString(conn, string):
#    print("sending: ",string)
    conn.sendall(string.encode())
    
def recString(conn):
    return conn.recv(4096).decode()

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

    while array[0][c] == 'o' or array[0][c] == 'x':   #if the column is full reassign
        c = random.randrange(6)

    while array[r][c] == 'o' or array[r][c] == 'x' and r > 0:            
        r-=1
    array[r][c] = 'x'

"""
Will check the board to see if the player or AI has connected 4
AI: token='x' mesg='You lose.'
returns a tuple (code, message)
code=1 => enter END state
code=0 => continue
"""
def checkEnd(token='o', mesg='You Win!'):
    r = 6
    c = 7
    for i in range(r):
        for j in range(c):
            # print("Array i's: "+ str(i) +" "+ array[i][j] + array[i-1][j] + array[i-2][j] + array[i-3][j])
            # print("Array j's: "+ str(j) +" "+ array[i][j] + array[i][j-1] + array[i][j-2] + array[i][j-3]) 
            # print(array[i][j], end='')

            #Check for Player win scenarios
            if i > 2:
                if array[i][j] == token and array[i-1][j] == token  and array[i-2][j] == token and array[i-3][j] == token: #if they have a vertical connect4
                    sendme = sendArr() + mesg + " (Vert)\n"
                    return (1,sendme)
            if j > 2:    
                if array[i][j] == token and array[i][j-1] == token  and array[i][j-2] == token and array[i][j-3] == token: #horizontal win, the if statement is to avoid a wrapping bug in which one could win with something like 4 5 6 0. 
                    sendme = sendArr() + mesg + " (Horiz)\n"
                    return (1,sendme)
            if j > 2 and i > 2:
                if array[i][j] == token and array[i-1][j-1] == token and array[i-2][j-2] == token and array[i-3][j-3] == token:
                    sendme = sendArr() + mesg + " (Diag: \\)\n" # double backslash to escape the escape char
                    return (1,sendme)
            if i > 2 and j < 5:
                if array[i][j] == token and array[i-1][j+1] == token and array[i-2][j+2] == token and array[i-3][j+3] == token:
                    sendme = sendArr() + mesg + " (Diag: /)\n"
                    return (1,sendme)
            return (0,"")

"""
Will check the board for a Draw / Full board
returns a tuple (code, message)
code=1 => enter END state
code=0 => continue
"""
def checkDraw():
    r = 6
    c = 7
    count = 0
    maxCount = r * c # 42
    for i in range(r):
        for j in range(c):
            if array[i][j] == 'o' or array[i][j] == 'x':
                count += 1
            j -= 1
        i -= 1
    #print("count: " + str(count))
    if count == maxCount:
        sendme = sendArr() + "Draw!\n"
        return (1,sendme)
    return (0,"")

if __name__ == "__main__":
    main()