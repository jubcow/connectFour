##Simple HTTP Server in python by Josh Butler

import socket
import select
import sys
import datetime
import os
import string

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

headerend = "\nDate: "+date+"\nServer: Josh Butler's Server\nContent-Type: text/html; charset=UTF-8\nContent-Length: " #helper string to reduce clutter
filefound = True

while True:
    try:
        conn,addr = sock.accept()
        print("Connection from:", addr)

        data = conn.recv(4096).decode() #Use conn.recv for a server, not sock.recv. 
        #print(data)
        line1 = data.split('\n',1)[0] #split the message so we get only the 1st line
        #print("First line: " + line1) #print to check

        #check if there are 3 words in line1 here, then return 400 error if not 3 words 
        tres = len(line1.split())
        if tres != 3:
            #print("test")
            sendme1 = "HTTP/1.1 400 Bad Request"+headerend+"100"+"\n\n<!DOCTYPE html><html><title>400 Error</title><center><body>400 Bad Request</body></center></html>"
            sendme1 = sendme1.encode()
            conn.send(sendme1)
            conn.close()

        request = line1.split(' ',3)[0] #Split first line up into 3 parts: the request method, file, protocol
        filename = line1.split(' ',3)[1]
        prot = line1.split(' ',3)[2]
        prot = prot.strip() #prot had a ton of whitespace characters 
        print("word1: "+request+" word2: "+filename+" word3: "+prot)
        print("file: "+filename+"\n")
        filename = filename.replace('/','')
        if filename == "":          #if the filename was just /, then set filename to index.html
            filename = "index.html"

        try:
            with open(filename,'r') as myfile: #have a string equal contents of file
                content = myfile.read()
                #print("Content found")
                filefound = True
        except PermissionError:     #If the file is found but unreadable
            #print("PERMISSIONERROR")
            sendme3 = "HTTP/1.1 403 Forbidden"+headerend+"100"+"\n\n<!DOCTYPE html><html><body><center>403 Forbidden</body></center></html>"
            sendme3 = sendme3.encode()
            conn.send(sendme3)
            conn.close()
            filefound = False
        except FileNotFoundError:
            #print("File not found...")
            sendme2 = "HTTP/1.1 404 Not Found"+headerend+"100"+"\n\n<!DOCTYPE html><html><title>404 Error</title><center><body>File not found</body></center></html>"
            sendme2 = sendme2.encode()
            conn.send(sendme2)
            conn.close()
            filefound = False
        except:
            #print("Test")
            filefound = False
            conn.close()


        if request != "GET":
            #print("405")
            senddata = "HTTP/1.1 405 Method Not Allowed"+headerend+"100"+"\n\n<!DOCTYPE html><html><body><center>405 Method Not Allowed</body></center></html>"
            senddata = senddata.encode()
            conn.sendall(senddata)
            conn.close()
        elif prot != "HTTP/1.1":
            #print("505")
            sendme4 = "HTTP/1.1 505 HTTP Version Not Supported"+headerend+"100"+"\n\n<!DOCTYPE html><html><body><center>505 HTTP Version Not Supported</body></center></html>"
            sendme4 = sendme4.encode()
            conn.send(sendme4)
            conn.close()
        elif request == "GET" and prot == "HTTP/1.1" and filefound:
            #print("Got file")
            sendme5 = "HTTP/1.1 200 OK"+headerend+str(len(content)+15)+"\n\n"+content #send code 200 and the file contents, using len to get content's length for protocol
            sendme5 = sendme5.encode()
            conn.send(sendme5)
            conn.close()
    except:
        sendme4 = "HTTP/1.1 500 Internal Server Error"+headerend+"100"+"\n\n<!DOCTYPE html><html><body><center>500 Internal Server Error</body></center></html>"
        sendme4 = sendme4.encode()
        conn.send(sendme4)
        conn.close()


