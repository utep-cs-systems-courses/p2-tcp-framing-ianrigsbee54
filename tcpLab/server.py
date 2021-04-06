#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from frameSock import frameRecv
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False),
    (('-d', '--debug'), "debug", False),
    )

progname = "server"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

debug = paramMap['debug']

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddress = ("127.0.0.1", listenPort)
s.bind(bindAddress)
s.listen(10)              # allow only one outstanding request
# s is a factory for connected sockets
os.chdir("./serverFiles") #for our transferred files
while True:
    print("awaiting connection")
    conn, addr = s.accept()
    if os.fork() == 0:
        print('Connected by', addr)
        try:
            print("waiting for client") #wait to receive file name and its contents
            fileName, fileData = frameRecv(conn) #start receiving file and its contents
            print("successful recv")
        except:
            print("failed transfer")
            conn.send(("0").encode())#failed to receive
            sys.exit(1)
        try:
            transferFile = open(fileName, "wb") #write in binary mode
            transferFile.write(fileData)
            transferFile.close()
        except:
            print("failed to write to file")
            conn.send(("0").encode())#failed to write
            sys.exit(1)
        conn.send(("1").encode())#successfully transfered file
        sys.exit(0)
        

