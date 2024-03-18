import cmd
import socket
import sys


class NetCmd(cmd.Cmd):
    prompt = "$ "

    def __init__(self, sockfd):
        super().__init__()
        self.sockfd = sockfd

    def do_print(self, arg):
        self.sockfd.sendall(("print " + arg).encode())
        print(sockfd.recv(1024).rstrip().decode())

    def do_info(self, arg):
        self.sockfd.sendall(("info " + arg).encode())
        print(sockfd.recv(1024).rstrip().decode())

    def do_exit(self, arg):
        print()
        return True

    do_EOF = do_exit

    def complete_info(self, text, line, begidx, endidx):
        return [s for s in ("host", "port") if s.startswith(text)]


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1336 if len(sys.argv) < 3 else int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
    sockfd.connect((host, port))
    NetCmd(sockfd).cmdloop()
