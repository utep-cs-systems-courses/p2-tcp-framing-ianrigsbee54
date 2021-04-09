import socket

class framedSock:
    def __init__(self, socket):
        self.sock = socket
        self.rbuff = b"" #make rbuff an attribute to prevent multiple threads from writing to one global buff

    def closeSock(self):
        self.sock.close()

    def sendStatus(self, status):
        self.sock.send(str(status).encode())

    def getStatus(self):
        status = self.sock.recv(100)
        return status.decode()
            
    def frameSend(self, fileName, fileData):
        msg = str(len(fileData)).encode() + b':' + fileName.encode() + b':' + fileData
        while len(msg):
            sentMsg = self.sock.send(msg)
            msg = msg[sentMsg:]

    def frameRecv(self):
        recvMessage = self.sock.recv(100)
        framedMessage = recvMessage.split(b':')
        msgLength = int(framedMessage[0])
        fileName = framedMessage[1].decode()
        self.rbuff += framedMessage[2]
        while True:
            if len(self.rbuff) >= msgLength:
                fileData = self.rbuff[0:msgLength]
                self.rbuff = self.rbuff[msgLength:]
                return fileName, fileData
            recvMessage = self.sock.recv(100)
            self.rbuff+=recvMessage
