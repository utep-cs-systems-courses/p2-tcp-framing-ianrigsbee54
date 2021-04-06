import re


def frameSend(sock, fileName, fileData):
    #frame ex:   filelength:test.txt:filedata
    msg = str(len(fileData)).encode() + b':' + fileName.encode() + b':' + fileData
    while len(msg):
        sentMsg = sock.send(msg)#continuously send file contents
        msg = msg[sentMsg:]#cut message length 


    
rbuff = b""
def frameRecv(sock):
    global rbuff
    recvMessage = sock.recv(100)
    framedMessage = recvMessage.split(b':')
    fileName = framedMessage[1].decode()
    msgLength = int(framedMessage[0])
    rbuff += framedMessage[2]
    while True:
        if len(rbuff) >= msgLength:
            fileData = rbuff[0:msgLength]
            rbuff = rbuff[msgLength:]
            return fileName, fileData
        recvMessage = sock.recv(100)
        rbuff+=recvMessage

