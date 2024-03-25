import socket
import sys
import readline
import threading


def readMsg(sockfd):
    while res := sockfd.recv(1024).rstrip():
        print(f"{res}\n{readline.get_line_buffer()}", end='', flush=True)


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    threading.Thread(target=readMsg, args=[s]).start()
    while msg := sys.stdin.buffer.readline():
        match msg.split(maxsplit=1):
            case ["hi"]:
                s.sendall(b"Hello everybody\n")
            case ["say", text]:
                s.sendall(text)
