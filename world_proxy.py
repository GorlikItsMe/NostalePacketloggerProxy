import socket
import sys
import threading
from noscrypto import Client, Server

INPUT_IP    = "127.0.0.1"
INPUT_PORT  = 4010
OUTPUT_IP   = "79.110.84.132"
OUTPUT_PORT = 4010

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
            try:
                conn.send(data)
            except OSError:
                break
        else:
            break
    print("Kill thread_recv")




sessionId = 0
def after_send_func_handler(data):
    global sessionId
    #packet = Server.LoginDecrypt(data).decode("ascii")
    if(sessionId == 0):
        packet = Server.WorldDecrypt(data, sessionId, True).decode("ascii")
        sessionId = int(packet.split(" ")[1])
        print("[SEND>>]", packet)
    else:
        packet = Server.WorldDecrypt(data, sessionId, False).decode("ascii")
        print("[SEND>>]", packet)

    return data

def after_recv_func_handler(data):
    output_raw = b''
    for packet_raw in data.split(b'\xff'): # rozbijanie zestawu pakietów
        if packet_raw == b'':
            break
        else:
            packet_raw+=b'\xff' # dodaj brakujący znak po rozbicu

        packet = Client.WorldDecrypt(packet_raw).decode("ascii")
        print("[RECV<<]", packet)

        output_raw += packet_raw
    
    return output_raw






if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('starting up world_proxy')
    sock.bind((INPUT_IP, INPUT_PORT))
    sock.listen(100)

    while True:
        print('waiting for a connection')
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
    
