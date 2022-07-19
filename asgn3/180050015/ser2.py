import socket

HOST = '20.1.1.1'
PORT = 25
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOCK_STREAM, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print('Address binded')
s.listen(1)

conn, addr = s.accept()
print('hello')

print('Connected by', addr)
data = conn.recv(1024)
if not data:
    print('no data received')
else:
    print('sending back to client')
    conn.sendall('Sending data: ' + data)
conn.close()
s.close()
exit(0)

