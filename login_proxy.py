import socket
import sys
import threading
from noscrypto import Client, Server

INPUT_IP    = "127.0.0.1"
INPUT_PORT  = 4000
OUTPUT_IP   = "79.110.84.75"
OUTPUT_PORT = 4004

def thread_send(conn, remote_sock, after_send_func):
    while (True):
        try:
            data = connection.recv(2048)
        except ConnectionAbortedError:
            break
        if data:
            data = after_send_func(data)
            remote_sock.send(data)
        else:
            break
    print("Kill thread_send")


def thread_recv(conn, remote_sock, after_recv_func):
    while (True):
        try:
            data = remote_sock.recv(2048)
        except ConnectionAbortedError:
            break
        if data:
            data = after_recv_func(data)
            conn.send(data)
        else:
            break
    print("Kill thread_recv")





def after_send_func_handler(data):
    packet = Server.LoginDecrypt(data).decode("ascii")
    print("[SEND>>]", packet)

    return data

def after_recv_func_handler(data):
    packet = Client.LoginDecrypt(data).decode("ascii")

    if packet.startswith('NsTeST'):
        ses = packet.split(" ")[2]
        p = "NsTeST username {0} 127.0.0.1:4010:1:1.1.GameFail 127.0.0.1:4010:1:2.1.Proxy -1:-1:-1:10000.10000.1".format(ses)
        print("[recv<<]", p)
        return Server.LoginEncrypt(p.encode("ascii"))
    
    print("[RECV<<]", packet)
    return data






if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Starting up login_proxy')
    sock.bind((INPUT_IP, INPUT_PORT))
    sock.listen(100)

    while True:
        print('Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('client connected:', client_address)
            remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_sock.connect((OUTPUT_IP, OUTPUT_PORT))

            
            t_recv = threading.Thread(target=thread_send, args=(connection, remote_sock, after_send_func_handler))
            t_recv.start()

            t_send = threading.Thread(target=thread_recv, args=(connection, remote_sock, after_recv_func_handler))
            t_send.start()

            while(True):
                if( t_recv.is_alive() ==False or t_send.is_alive() ==False ):
                    print("Disconnect")
                    break
        #except Exception as e:
        #    print(e)
        finally:
            connection.close()
    
