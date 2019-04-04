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
	    print(data)
	    formatted = False
	    while formatted == False:
	        msg = input("Enter a number 0-6\n")
	        if not (int(msg) > 6 or int(msg) < 0):
	            formatted = True
	            
	    send = msg.encode()
	    sock.sendall(send)
