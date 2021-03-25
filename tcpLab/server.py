#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets
rbuff = b""
def frameRecv(sock):
    global rbuff
    state = 1
    msgLength = 0
    while true:
        if state == 1:
            match = re.match(b'([^:]+):(.*):(.*)'.rbuff, re.DOTALL | re.MULTILINE) #use regex
            if match:
                strLength, fileName, rbuff = match.groups()
                try:
                    msgLength = int(strLength)
                except:
                    if len(rbuff):
                        os.write(2, ("message incorrectly formatted").encode())
                        return None, None
                state = 2
        if state == 2:
            fileData = rbuff[0:msgLength]
            rbuff = rbff[msgLength:]
            return fileName, fileData
        leftover = sock.recv(1024)
        rbuff+= leftover
        if len(rbuff) != 0:
            os.write(2, ("incomplete message").encode())
            return None
while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)
        try:
            fileName, fileData = frameRecv(s)
        except:
            os.write(2, ("failed to receive message").encode())
            sys.exit(1)
        fileName = fileName.decode()
        os.write(2, ("received file %s" % fileName).encode())
        try:
            transferFile = os.open(fileName, os.O_WRONLY | os.O_CREAT)
            os.write(transferFile, fileData)
            os.close(transferFile)
        except:
            os.write(2, ("failed to write to file").encode())
            s.send(("0").encode())#failed
        s.send(("1").encode())#passed
            


