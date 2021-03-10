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

def frameSend(sock, fileData):
    msg = str(len(fileData)).encode() + b':' + fileData.encode()
    sentMsg = sock.send(msg)
    os.write(1, ("sending %d byte message" % len(fileData)).encode())
    
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
fileNameSent = False
while 1:
    fileName = input("enter file name")
    fileName.strip()
    if fileName != "exit":
        if os.path.isfile(fileName):
            s.send(fileName.encode())
            received = s.recv(1024).decode()
            os.write(1, ("received: '%s'\n" % received).encode())
            fileNameSent = True
        else:
            os.write(1, ("file doesnt exist, try again").encode())
            sys.exit(0)
        if fileNameSent == True:
            file = open(fileName, 'r')
            fileData = file.read()
            frameSend(s, fileData)
            file.close()
    else:
        os.write(1, ("exiting").encode())
        sys.exit(0)
    break
print("Zero length read.  Closing")
s.close()
