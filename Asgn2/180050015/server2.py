import socket

HOST = '192.168.122.3'
PORT = 3000
low = 100000
high = 1000000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            i = 0
            if not data:
                break
            elif data ==b'low':
                for _ in range(low):
                    i += 1

            elif data == b'high':
                for _ in range(high):
                    i += 1  
            conn.sendall(str(i).encode())