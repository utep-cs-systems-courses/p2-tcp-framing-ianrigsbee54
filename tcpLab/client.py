#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

def frameSend(sock, fileName, fileData):
    msg = str(len(fileData)).encode() + b':' + fileName.encode() + b':' + fileData.encode()
    while len(msg):
        sentMsg = sock.send(msg)
        msg = msg[sentMsg:]
    
if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")
    
FILE_PATH ="clientFiles/"

while True:
    fileName = os.read(0, 1024).decode()
    fileName.strip()
    if fileName != "exit":
        if os.path.exists(FILE_PATH + fileName):
            file = open(FILE_PATH + fileName, "rb")
            fileData = file.read()
            if len(fileData) <= 0:
                os.write(2, ("file is empty").encode())
                continue
            frameSend(s, fileName, fileData)
        else:
            os.write(2, ("file doesnt exist, try again").encode())
            sys.exit(1)
    else:
        os.write(1, ("exiting").encode())
        s.close()
        sys.exit(0)
