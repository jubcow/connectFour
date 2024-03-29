#!/bin/python3
"""
Connect Four client/server program (Server portion)
@author Joshua Butler
@author John Pruchnic
@date 4/16/2019

I hereby declare upon my word of honor that I have neither given nor received unauthorized help on this work.
"""

import socket
import random
import json
import sys
import threading

a = {}
try:
    with open('addresses.json') as server_json:
        a = json.load(server_json)
        print(a)
except FileNotFoundError:
    print("""Can't find 'addresses.json' - this must contain your IP information!
Match the form:

{
    "SERVER": {
        "INTERNAL":"10.142.0.2",
        "EXTERNAL":"35.185.114.102",
        "PORT":"4040"
    }
}""")
    sys.exit()

#now = datetime.datetime.now(datetime.timezone.utc)
#date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
HOST = a["SERVER"]["INTERNAL"]
PORT = int(a["SERVER"]["PORT"])

ROWS = 6
COLS = 7

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#reuse address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind host IP and port to server socket
sock.bind((HOST, PORT))

def main():
    threadCount = 0
    while True:
        sock.listen()
        print("threads alive:",threading.active_count())
        conn,addr = sock.accept()
        gameT = gameThread(threadCount, conn, addr)
        gameT.start()
        threadCount += 1
        
    
class gameThread(threading.Thread):
    """Class gameThread is instantiated to run a game session for each connected client
    """
    def __init__(self, threadID, conn, addr):
        """constructor requires a threadID, the connection object, and the client's address
        """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conn = conn
        self.addr = addr
    def run(self):
        """method that runs when start() is called on the gameThread object, runs the game logic
        """
        print("Starting game thread id: ",self.threadID," with ",self.addr)
        playGame(self.conn, self.addr, self.threadID)
        return self.threadID
        

def playGame(conn, addr, threadID):
    
    try:
        #Array Declaration with no moves made
        array = [['-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-']]

        sendme = sendArr(array) # send current board
        sendString(threadID, conn, sendme)

        end = False
        while not end:

            # get player input / turn
            data = recString(conn) #Use conn.recv for a server, not sock.recv.
            print("ThreadID:",threadID,"received:",data)

            # client side input validation
            while not goodInput(data) or not legalMove(array, data):
                try:
                    sendme = sendArr(array, "Illegal Move")
                    sendString(threadID, conn, sendme)
                    data = recString(conn)
                    print("ThreadID:",threadID,"received:",data)
                except BrokenPipeError:
                    end = True
                    break

            if not end:
                r = 5
                c = int(data)
                while array[r][c] == 'o' or array[r][c] == 'x' and r > 0: # drop token 'x' represents the AI, 'o' is player
                    r-=1
                array[r][c] = 'o'

                #checks
                endRes = checkEnd(array, 'o', 'You Win!') #Check if the player has won
                if endRes[0] == 0: # previous check was code=0 'CONTINUE'
                    endRes = checkDraw(array) # check for draw
                if endRes[0] == 1: # previous check was code=1 'END STATE'
                    sendString(threadID, conn, endRes[1]) # endRes[1] contains message to send
                    end = True

                if not end:
                    #AI takes turn after player
                    aiTurn(threadID, array)

                    # checks
                    endRes = checkEnd(array, 'x', 'You lose.') #Check if the AI has won
                    if endRes[0] == 0: # previous check was code=0 'CONTINUE'
                        endRes = checkDraw(array) # check for draw
                    if endRes[0] == 1: # previous check was code=1 'END STATE'
                        sendString(threadID, conn, endRes[1]) # endRes[1] contains message to send
                        end = True

                    if endRes[0] == 0: # if any of the above returned code=0 'CONTINUE'
                        sendme = sendArr(array) # send current board
                        sendString(threadID, conn, sendme)

        conn.close()
        print("Connection to" ,addr,"Closed")
    except OSError:
        pass

def sendString(threadID, conn, string):
    """Helpful wrapper for the socket sending
    """
    print("ThreadID:",threadID,"sending:",string)
    conn.sendall(string.encode())
    
def recString(conn):
    """Helpful wrapper for the socket receiving
    """
    return conn.recv(4096).decode()

def goodInput(inp):
    """Boolean function to validate input
    """
    try:
        x = int(inp)
    except:
        return 0
    if not x in range(COLS):
        return 0
    return 1

def legalMove(array, c):
    """Boolean function to check if column c is full
    """
    if array[0][int(c)] == '-':
        return 1
    else:
        return 0

def sendArr(array, forced_mesg=""):
    """Function that puts the current array into a string and returns the string to be sent to the client. 
    """
    ArrayString = ""
    for i in array:
        for j in i:
            ArrayString = ArrayString + j
    return ArrayString + "#" + forced_mesg

def aiRandomTurn(array):
    """Function to compute a random valid turn for the AI
    """
    r = 5
    c = random.randrange(0, 7, 1)

    while array[0][c] == 'o' or array[0][c] == 'x':   #if the column is full reassign
        c = c = random.randrange(0, 7, 1)

    while array[r][c] == 'o' or array[r][c] == 'x' and r > 0:
        r-=1
    array[r][c] = 'x'

def aiTurn(threadID, array,token = 'x'):
    """Function for AI taking a turn, AI will check for possible win conditions it could take
    """
    aiDone = False

    for i in range(ROWS):
        for j in range(COLS):
            #Check for possible player wins and block
            if i > 2:
                if array[i][j] == 'o' and array[i-1][j] == 'o'  and array[i-2][j] == 'o' and array[i-3][j] != 'o' and array[i-3][j] != 'x' and aiDone == False: #vertical
                    array[i-3][j] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Vertical block")
            if j > 2 and i < ROWS-1:
                if array[i][j] == 'o' and array[i][j-1] == 'o'  and array[i][j-2] == 'o' and array[i][j-3] != 'o' and array[i][j-3] != 'x' and array[i+1][j-3] != '-' and aiDone == False:
                    array[i][j-3] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Horizontal Block Left")
            if j > 2 and i == ROWS-1:                 
                if array[i][j] == 'o' and array[i][j-1] == 'o'  and array[i][j-2] == 'o' and array[i][j-3] != 'o' and array[i][j-3] != 'x' and aiDone == False:
                    array[i][j-3] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Horizontal Block Left Bottom Row")
            if j < 4 and i < ROWS-1:
                if array[i][j] == 'o' and array[i][j+1] == 'o'  and array[i][j+2] == 'o' and array[i][j+3] != 'o' and array[i][j+3] != 'x' and array[i+1][j+3] != '-' and aiDone == False:
                    array[i][j+3] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Horizontal Block Right")
            if j < 4 and i == ROWS-1:
                if array[i][j] == 'o' and array[i][j+1] == 'o'  and array[i][j+2] == 'o' and array[i][j+3] != 'o' and array[i][j+3] != 'x' and aiDone == False:
                    array[i][j+3] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Horizontal Block Right Bottom Row")
            if j > 2 and i > 2:
                if array[i][j] == 'o' and array[i-1][j-1] == 'o' and array[i-2][j-2] == 'o' and array[i-3][j-3] != 'o' and array[i-3][j-3] != 'x' and array[i-2][j-3] != '-' and aiDone == False:
                    array[i-3][j-3] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Diag Block")
            if i > 2 and j < 4:
                if array[i][j] == 'o' and array[i-1][j+1] == 'o' and array[i-2][j+2] == 'o' and array[i-3][j+3] != 'o' and array[i-3][j+3] != 'x' and array[i-2][j+3] != '-' and aiDone == False:
                    array[i-3][j+3] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Diag Block2")
    
    for i in range(ROWS):
        for j in range(COLS):
            #print(array[i][j] + " " + array + " " + array[i][j-1] + " " + array[i][j-2])
            #Check for possible wins
            if i > 2:
                if array[i][j] == token and array[i-1][j] == token  and array[i-2][j] == token and array[i-3][j] == '-' and aiDone == False: #vertical
                    array[i-3][j] = 'x'
                    print("ThreadID:",threadID," AI move: Vert win")
                    aiDone = True
            if j > 2 and i == ROWS-1:
                if array[i][j] == token and array[i][j-1] == token  and array[i][j-2] == token and array[i][j-3] == '-' and aiDone == False:
                    array[i][j-3] = 'x'
                    print("ThreadID:",threadID," AI move: Horiz win Bottom row")
                    aiDone = True
            if j > 2 and i < ROWS-1:
                if array[i][j] == token and array[i][j-1] == token  and array[i][j-2] == token and array[i][j-3] == '-' and array[i+1][j-3] != '-' and aiDone == False:
                    array[i][j-3] = 'x'
                    print("ThreadID:",threadID," AI move: Horiz win 1")
                    aiDone = True
            if j < 4 and i < ROWS-1:
                if array[i][j] == token and array[i][j+1] == token  and array[i][j+2] == token and array[i][j+3] == '-' and array[i+1][j+3] != '-' and aiDone == False:
                    array[i][j+3] = 'x'
                    print("ThreadID:",threadID," AI move: Horiz win 2")
                    aiDone = True
            if j > 2 and i > 2:
                if array[i][j] == token and array[i-1][j-1] == token and array[i-2][j-2] == token and array[i-3][j-3] == '-' and array[i-2][j-3] != '-' and aiDone == False:
                    array[i-3][j-3] = 'x'
                    print("ThreadID:",threadID," AI move: Diag win")
                    aiDone = True
            if i > 2 and j < 3:
                if array[i][j] == token and array[i-1][j+1] == token and array[i-2][j+2] == token and array[i-3][j+3] == '-' and array[i-2][j+3] != '-' and aiDone == False:
                    array[i-3][j+3] = 'x'
                    print("ThreadID:",threadID," AI move: Diag win2")
                    aiDone = True
    for i in range(ROWS):
        for j in range(COLS):
            #Check for possible short lines
            if i > 1:
                if array[i][j] == token and array[i-1][j] == token and array[i-2][j] == '-' and aiDone == False: #vertical
                    array[i-2][j] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Short vert")
            if j > 1 and i == ROWS-1:
                if array[i][j] == token and array[i][j-1] == token and array[i][j-2] == '-' and aiDone == False:
                    array[i][j-2] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Short horiz Bottom row")
            if j > 1 and i < ROWS-1:
                if array[i][j] == token and array[i][j-1] == token and array[i][j-2] == '-' and array[i+1][j-2] != '-' and aiDone == False:
                    array[i][j-2] = 'x'
                    aiDone = True
                    print("ThreadID:",threadID," AI move: Short horiz")


            """if j > 1 and i > 1:
                if array[i][j] == token and array[i-1][j-1] == token and array[i-2][j-2] == '-' and array[i-2][j-1] != '-' and aiDone == False:
                    array[i-2][j-2] = 'x'
                    aiDone = True
                    print("Short diag")
            if i > 1 and j < 2:
                if array[i][j] == token and array[i-1][j+1] == token and array[i-2][j+2] == '-' and array[i-2][j+3] != '-' and aiDone == False:
                    array[i-2][j+2] = 'x'
                    aiDone = True
                    print("Short diag2")"""

    #If the AI hasn't found a win condition it can take, then randomly select
    if aiDone == False:
        print("ThreadID:",threadID," AI move: CHOOSING RANDOMLY");
        aiRandomTurn(array)
        aiDone = True

def checkEnd(array, token='o', mesg='You Win!'):
    """Will check the board to see if the player or AI has connected 4
        AI: token='x' mesg='You lose.'
        returns a tuple (code, message)
        code=1 => enter END state
        code=0 => continue
    """
    code = 0
    sendme = ""
    for i in range(ROWS):
        for j in range(COLS):
            #Check for win scenarios
            if i > 2:
                if array[i][j] == token and array[i-1][j] == token  and array[i-2][j] == token and array[i-3][j] == token: #if they have a vertical connect4
                    sendme = sendArr(array) + mesg + " (Vert)\n"
                    code = 1
                    break
            if j > 2:    
                if array[i][j] == token and array[i][j-1] == token  and array[i][j-2] == token and array[i][j-3] == token: #horizontal win, the if statement is to avoid a wrapping bug in which one could win with something like 4 5 6 0. 
                    sendme = sendArr(array) + mesg + " (Horiz)\n"
                    code = 1
                    break
            if j > 2 and i > 2:
                if array[i][j] == token and array[i-1][j-1] == token and array[i-2][j-2] == token and array[i-3][j-3] == token:
                    sendme = sendArr(array) + mesg + " (Diag: \\)\n" # double backslash to escape the escape char
                    code = 1
                    break
            if i > 2 and j < 4:
                if array[i][j] == token and array[i-1][j+1] == token and array[i-2][j+2] == token and array[i-3][j+3] == token:
                    sendme = sendArr(array) + mesg + " (Diag: /)\n"
                    code = 1
                    break
            if code == 1:
                break
    return (code, sendme)


def checkDraw(array):
    """Checks the board for a Draw / Full board.
        returns a tuple (code, message)
        code=1 => enter END state
        code=0 => continue
    """
    count = 0
    maxCount = ROWS * COLS # 42
    for i in range(ROWS):
        for j in range(COLS):
            if array[i][j] == 'o' or array[i][j] == 'x':
                count += 1
    #print("count: " + str(count))
    if count == maxCount:
        sendme = sendArr(array) + "Draw!\n"
        return (1,sendme)
    return (0,"")

if __name__ == "__main__":
    main()
