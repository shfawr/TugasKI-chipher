import socket, threading
from cipher import encrypt, decrypt

SHARED_KEY = "keamanan"
HOST = '0.0.0.0'
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
    while True:
        ciphertext = recv_message(sock)
        if not ciphertext:
            print("putus")
            break
        print("cipher :", ciphertext.hex())
        try:
            print("asli   :", decrypt(ciphertext, SHARED_KEY))
        except:
            print("gagal decrypt")
        print("> ", end='', flush=True)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print("menunggu koneksi...")

    conn, addr = server.accept()
    print("masuk dari", addr)

    threading.Thread(target=receive_loop, args=(conn,), daemon=True).start()

    while True:
        msg = input("> ")
        if msg == "exit": break
        cipher = encrypt(msg, SHARED_KEY)
        print("cipher :", cipher.hex())
        send_message(conn, cipher)

    conn.close()
    server.close()

main()