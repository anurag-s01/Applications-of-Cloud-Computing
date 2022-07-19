import socket
import threading
import time

HOST1 = '192.168.122.2'  # The server's hostname or IP address
HOST2 = '192.168.122.3'  # The server's hostname or IP address
localhost = '127.0.0.1'
localport = 5000
PORT = 3000        # The port used by the server
iterations = 0
numserver = 1
currserver = 0
mode = 0
quit = 0 
sockets = []
def work(lock):
    global iterations, currserver
    while True:
        iterations += 1
        s = sockets[currserver]
        lock.acquire()
        if (mode == 1):
            s.sendall(b'high')
        else:
            s.sendall(b'low')
        lock.release()
        s.recv(1024)
        currserver += 1
        lock.acquire()
        currserver %= numserver
        lock.release()
        time.sleep(0.01)
        lock.acquire()
        if (quit):
            break
        lock.release()
    lock.release()
    return

def listen_for_keyboard(lock):
    global mode
    global quit
    while True:
        if (mode == 0):
            m = 'low'
        else:
            m = 'high'
        print('Mode = '+m)
        a = input('Enter "s" to switch between modes and "x" to exit: ')
        if (a == 's'):
            lock.acquire()
            mode = 1 - mode
            lock.release()
        if (a == 'x'):
            lock.acquire()
            quit = 1
            lock.release()
            break
        print()
    lock.acquire()
    if (numserver == 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((localhost, localport))
            s.sendall(b'exit')
    lock.release()
    return

def listen_for_server(lock):
    global numserver
    global sockets
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((localhost, localport))
        s.listen()
        conn, _ = s.accept()
        with conn:
            data = conn.recv(1024)
            if data == b'available':
                while True:
                    try:
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s2.connect((HOST2, PORT))
                        sockets.append(s2)
                        lock.acquire()
                        numserver += 1
                        lock.release()
                        break
                    except Exception:
                        # print('Not connected yet', flush=True)
                        continue
            elif data == b'exit':
                return

if __name__ == "__main__":
    lock = threading.Lock()
    t1 = threading.Thread(target=work, args=(lock,))
    t2 = threading.Thread(target=listen_for_keyboard, args=(lock,))
    t3 = threading.Thread(target=listen_for_server, args=(lock,))
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((HOST1, PORT))
    sockets.append(s1)
    t3.start()
    t1.start()
    t2.start()
    

    t1.join()
    t2.join()
    t3.join()
    for s in sockets:
        s.close()
