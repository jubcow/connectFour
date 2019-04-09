#!/bin/python3
"""
Connect Four client/server program (Client portion)
@author Joshua Butler
@author John Pruchnic

I hereby declare upon my word of honor that I have neither given nor received unauthorized help on this work.
"""

import socket
import select
import sys
import re
import json

a = {} # initialize to empty dictionary
try:
    with open('addresses.json') as server_json:
        a = json.load(server_json)
except FileNotFoundError:
    print("file not found!")
    sys.exit()

# host (external) IP address and port
HOST = a["SERVER"]["EXTERNAL"]
PORT = int(a["SERVER"]["PORT"])

ROWS = 6
COLS = 7

END_GAME = False

def main():
    # create our socket using with, to clean up afterwards
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST,PORT))#Initial connection being made using the IP address of the server and correct port number
            print("connected to ",HOST,":",PORT)
        except:
            print('Not connected\n')
            sys.exit()
        while not END_GAME:
            data = recString(sock);
            print("received: " + data) # debug
            print(makePretty(data))
            if not END_GAME:
                msg = input(" Enter a number 0-6 : ")
                while not goodInput(msg):
                    msg = input(" Enter a number 0-6 : ")
                    
                sendString(sock, msg)

def makePretty(arrayStr):
    """Build a pretty representation of the current layout 
          ___________________________
         |   |   |   |   |   |   |   |
         |---|---|---|---|---|---|---|
         |   |   |   |   |   |   |   |
         |---|---|---|---|---|---|---|
         |   |   |   |   |   |   |   |
         |---|---|---|---|---|---|---|
         |   |   |   |   |   |   |   |
         |---|---|---|---|---|---|---|
         |   |   |   |   |   |   |   |
         |---|---|---|---|---|---|---|
         _____________________________
         | 0 | 1 | 2 | 3 | 4 | 5 | 6 |

         !!! BEHOLD INSANITY BELOW !!!
    """
    global END_GAME
    # deterine char and color of tokens
    ENEMY_TOKEN = tc.CEND + tc.CBOLD + tc.CRED  + "O" + tc.CEND + tc.CBLUE 
    BUDDY_TOKEN = tc.CEND + tc.CBOLD + tc.CBLUE2 + "O" + tc.CEND + tc.CBLUE 

    # generate pretty board around data of dimensions COLS and ROWS
    top     = "  " + (COLS-1)*"____" + "___ \n"
    divider = " |" + COLS*"---|" + "\n"
    bottom  = " _" + COLS*"____" + "\n"
    numbers = " |" + ''.join([" "+str(x)+" |" for x in range(COLS)]) + "\n"
    array = [ ''.join([" | " + str(arrayStr[COLS*j + i]) for i in range(COLS)]) + " | \n" for j in range(ROWS)]
    prettyStr = tc.CBLUE + top + divider.join(array) + divider + tc.CEND + tc.CBOLD + tc.CBLUE + bottom + numbers + tc.CEND

    # subsitute known tokens with pretty colorized versions
    prettyStr = prettyStr.replace(' - ', '   ')
    prettyStr = prettyStr.replace('x', ENEMY_TOKEN)
    prettyStr = prettyStr.replace('o', BUDDY_TOKEN)

    message = arrayStr.split("#")[1]
    if not message == "":
        if "win" in message.lower():
            END_GAME = True
            message = "\n   " + tc.CBOLD + tc.CGREEN + message + tc.CEND
        elif "lose" in message.lower():
            END_GAME = True
            message = "\n   " + tc.CBOLD + tc.CRED + message + tc.CEND
        else:
            message = "\n   " + tc.CBOLD + tc.CYELLOW + message + tc.CEND

    return prettyStr + message

def goodInput(inp): # returns boolean
    try:
        x = int(inp)
    except:
        return 0
    if not x in range(COLS):
        return 0
    return 1

class tc:
    """text color
        extended ascii color codes. used to color the tokens
        gathered from stackoverflow answers:
        https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
    """
    #TODO remove unused color codes (wait till done)
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    
    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE  = '\33[36m'
    CWHITE  = '\33[37m'
    
    CBLACKBG  = '\33[40m'
    CREDBG    = '\33[41m'
    CGREENBG  = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG   = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG  = '\33[46m'
    CWHITEBG  = '\33[47m'
    
    CGREY    = '\33[90m'
    CRED2    = '\33[91m'
    CGREEN2  = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2   = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2  = '\33[96m'
    CWHITE2  = '\33[97m'
    
    CGREYBG    = '\33[100m'
    CREDBG2    = '\33[101m'
    CGREENBG2  = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2   = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2  = '\33[106m'
    CWHITEBG2  = '\33[107m'

def sendString(sock, string):
    """Helpful wrappers for the socket sending
        sock is in the global scope 
    """
    sock.sendall(string.encode())
    
def recString(sock):
    """Helpful wrappers for the socket recieving.
        sock is in the global scope 
    """
    return sock.recv(4096).decode()

if __name__ == "__main__":
    main()
