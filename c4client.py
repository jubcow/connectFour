#!/bin/python3
"""
Connect Four client/server program (Client portion)
@author Joshus Butler
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

def makePretty(arrayStr):
    """   ___________________________
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
    # deterine char and color of tokens
    ENEMY_TOKEN = tc.CBOLD + tc.CRED  + "O" + tc.CEND
    BUDDY_TOKEN = tc.CBOLD + tc.CBLUE + "O" + tc.CEND

    print("arrayStr: "+arrayStr)

    # generate pretty board around data of variables COLS and ROWS
    top     = "  " + (COLS-1)*"____" + "___ \n"
    divider = " |" + COLS*"---|" + "\n"
    bottom  = " _" + COLS*"____" + "\n"
    numbers = " |" + ''.join([" "+str(x)+" |" for x in range(COLS)]) + "\n"
    array = [ ''.join([" | " + str(arrayStr[COLS*j + i]) for i in range(COLS)]) + " | \n" for j in range(ROWS)]
    prettyStr = top + divider.join(array) + divider + bottom + numbers

    # subsitute known chars with pretty colorized versions
    prettyStr = prettyStr.replace(' - ', '   ')
    prettyStr = prettyStr.replace('x', ENEMY_TOKEN)
    prettyStr = prettyStr.replace('o', BUDDY_TOKEN)

    return prettyStr

def sanitizeInp(inp):
    None

class tc:
    """text color
        extended ascii color codes. used to color the coins
        gathered from stackoverflow answers:
        https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
    """
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



#TODO Add TKinter GUI, can have buttons to send 0-6 to server and a text display for the board text.
# create our socket using with, to clean up afterwards
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	try:
	    sock.connect((HOST,PORT))#Initial connection being made using the IP address of the server and correct port number
	    print("connected to ",HOST,":",PORT)
	except:
	    print('Not connected\n')
	    sys.exit()
	while True:
	    data = sock.recv(1024)
	    data = data.decode()
	    print(makePretty(data))
	    formatted = False
	    while formatted == False:
	        msg = input("Enter a number 0-6\n")
	        if not (int(msg) > 6 or int(msg) < 0):
	            formatted = True
	            
	    send = msg.encode()
	    sock.sendall(send)

