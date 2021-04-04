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
    state = 1
    msgLength = -1
    while True:
        if state == 1:
            #use regex to split string into three parts for our variables
            match = re.match(b'([^:]+):(.*):(.*)', rbuff, re.DOTALL | re.MULTILINE)
            if match:
                strLength, fileName, rbuff = match.groups()#set variables from regex groups
                try:
                    msgLength = int(strLength)
                except:
                    if len(rbuff):
                        print("message incorrectly formatted")
                        return None, None
                state = 2
        if state == 2: #start sending file contents and file name
            if len(rbuff) >= msgLength: #once we have all file content. Send it
                fileData = rbuff[0:msgLength]
                rbuff = rbuff[msgLength:]
                return fileName, fileData
        recMessage = sock.recv(1024) #receive data and put it in buffer 
        rbuff += recMessage
        if len(recMessage) == 0:#if nothing received and buffer still has content. Then quit
            if len(rbuff) != 0:
                print("incomplete message")
            return None, None
