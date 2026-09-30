import socket
import threading
from cipher import encrypt, decrypt

SHARED_KEY = "keamanan"
HOST = '127.0.0.1'
PORT = 5000

def recv_message(sock):
    data = b''
    while not data.endswith(b'\n'):
        c = sock.recv(1)
        if not c: return b''
        data += c
    return data[:-1]

def send_message(sock, payload):
    sock.sendall(payload + b'\n')

def receive_loop(sock):
    while 1:
        cipher = recv_message(sock)
        if not cipher:
            print("putus")
            break
        print("cipher :", cipher.hex())
        try:
            print("asli   :", decrypt(cipher, SHARED_KEY))
        except:
            print("gagal decrypt")
        print("> ", end='', flush=True)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("connected")

    threading.Thread(target=receive_loop, args=(client,), daemon=True).start()

    while 1:
        msg = input("> ")
        if msg == "exit": break
        c = encrypt(msg, SHARED_KEY)
        print("cipher :", c.hex())
        send_message(client, c)

    client.close()

main()