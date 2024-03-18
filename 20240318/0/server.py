import multiprocessing
import shlex
import socket
import sys


def serve(conn, addr):
    with conn:
        print(f"Connected with {addr[0]}:{addr[1]}")
        while data := conn.recv(1024):
            args = shlex.split(data.decode())
            match args[:2]:
                case ["print", _]:
                    conn.sendall(' '.join(args[1:]).encode())
                case ["info", "host"]:
                    conn.sendall(addr[0].encode())
                case ["info", "port"]:
                    conn.sendall(str(addr[1]).encode())
        print(f"Disconnected from {addr[0]}:{addr[1]}")


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1336 if len(sys.argv) < 3 else int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
    sockfd.bind((host, port))
    sockfd.listen()
    while True:
        conn, addr = sockfd.accept()
        multiprocessing.Process(target=serve, args=(conn, addr)).start()
