#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from frameThreads import framedSock
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
    
FILE_PATH ="clientFiles/"
fSock = framedSock(s)

while True:
    print("enter file name")
    fileName = os.read(0, 1024).decode()
    filePath = (FILE_PATH + fileName).strip()
    if fileName != "exit":
        if os.path.isfile(filePath):
            print("sending file contents")
            file = open(filePath, "rb")
            fileData = file.read()
            if len(fileData) < 1:
                print("empty file")
                continue
            fSock.frameSend(fileName, fileData)
        else:
            print("file doesnt exist try again")
            sys.exit(1)
        status = int(fSock.getStatus())
        if status == 1:
            print("server received file")
            fSock.closeSock()
            sys.exit(0)
        else:
            print("server failed in receiving file")
            fSock.closeSock()
            sys.exit(1)
    else:
        print("exiting")
        fSock.closeSock()
        sys.exit(0)
