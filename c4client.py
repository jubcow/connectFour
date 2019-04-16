#!/bin/python3
"""
Connect Four client/server program (Client portion)
@author Joshua Butler
@author John Pruchnic
@date 4/16/2019

I hereby declare upon my word of honor that I have neither given nor received unauthorized help on this work.
"""

import socket
import sys
import json

a = {} # initialize to empty dictionary
try:
    with open('addresses.json') as server_json:
        a = json.load(server_json)
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
            # print("received: " + data) # debug
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
    prettyStr = ""
    message = ""

    if arrayStr == "":
    	message = "\n   " + tc.CBOLD + tc.CYELLOW + "Server provided invalid response, exiting..." + tc.CEND
    	END_GAME = True
    else:
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

class tc:
    """text color
        Extended ascii color codes are used to color the tokens.
    """
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CBLUE2   = '\33[94m'

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
