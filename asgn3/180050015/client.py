import socket
import sys

HOST = ''

if (sys.argv[1] == '0'):
    HOST = '10.1.1.1'
elif (sys.argv[1] == '1'):
    HOST = '20.1.1.1'
else:
    print('Invalid server number')

PORT = 25

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = b'Hi there, how are u doing'
s.sendall(msg)
data = s.recv(1024)
print(data)
s.close()
