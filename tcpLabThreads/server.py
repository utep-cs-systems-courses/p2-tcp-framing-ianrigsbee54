#!/usr/bin/env python3
import socket, sys, os, time, threading
sys.path.append("../lib")       # for params
import params
from frameThreads import framedSock
from threading import Thread
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

lock = threading.Lock()
os.chdir("./serverFiles")
class Server(Thread):
    def __init__(self, connection, address):
        Thread.__init__(self) #prevents breaking instances
        self.conn = connection
        self.addr = address


    def run(self):
        global lock
        fSock = framedSock(self.conn)
        print("connected by", self.addr)
        while True:
            try:
                print("waiting for client")
                fileName, byteData = fSock.frameRecv()
                print("successful recv")
            except:
                print("failed transfer")
                fSock.sendStatus(0)#failed to receive
                sys.exit(1)
            lock.acquire() #placed aquire here so threads wont write to same file at the same time
            try:
                fileData = byteData.decode()
                transferFile = open(fileName, "w")
                transferFile.write(fileData)
                transferFile.close()
            except:
                print("failed to write to file")
                fSock.sendStatus(0)#failed to write
            lock.release() #once one thread is finished the other thread can write to file
            fSock.sendStatus(1)#successfully transfered file
            sys.exit(0)
    
if __name__ == "__main__":
    while True:
        conn, addr = s.accept()
        server = Server(conn, addr)
        server.start()

