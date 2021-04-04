#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time, os
sys.path.append("../lib")       # for params
import params
from frameSock import frameSend
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "client"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
port = (serverHost, serverPort)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(port)

if s is None:
    print('could not open socket')
    sys.exit(1)
    
FILE_PATH ="clientFiles/" #for our client files

while True:
    print("enter file name")
    fileName = os.read(0, 1024).decode()
    filePath = (FILE_PATH + fileName).strip()
    if fileName != "exit":
        if os.path.isfile(filePath):#check whole path if the file is a file.
            print("sending file contents")
            file = open(filePath, "rb")#read in binary mode
            fileData = file.read()
            if len(fileData) < 1: #cant handle empty files
                print("empty file, try again")
                continue
            frameSend(s, fileName, fileData)#send file and file contents
        else:
            print("file doesnt exist try again")
            s.close() #close connection in order to open it up 
            sys.exit(1)
        if int(s.recv(1024).decode()) == 1: #if successful transfer
            print("server received file")
            s.close()
            sys.exit(0)
        else:#if unsuccessful transfer
            print("server failed in receiving file")
            s.close()
            sys.exit(1)
    else:
        print("exiting")
        s.close()
        sys.exit(0)
