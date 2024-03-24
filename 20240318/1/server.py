import cmd
import cowsay
import shlex
import socket
import sys
from custom import custom


class Player:
    def __init__(self, x: int = 0, y: int = 0):
        assert 0 <= x <= 9 and 0 <= y <= 9, "Invalid initial position"
        self.x, self.y = x, y

    def move(self, dx, dy):
        self.x = (self.x + dx) % 10
        self.y = (self.y + dy) % 10
        return str(self.x), str(self.y), *encounter(self.x, self.y)

    def attack(self, name, damage):
        if (self.x, self.y) not in monsters:
            return '-1', '-1'
        if monsters[self.x, self.y].name != name:
            return '-1', '-1'
        damage = min(monsters[self.x, self.y].hp, damage)
        monsters[self.x, self.y].hp -= damage
        if monsters[self.x, self.y].hp == 0:
            del monsters[self.x, self.y]
            return '0', str(damage)
        return str(monsters[self.x, self.y].hp), str(damage)


p1 = Player()


class Monster:
    def __init__(self, name: str, text: str, hp: int):
        self.name, self.text, self.hp = name, text, hp


monsters = {}


def encounter(x, y):
    if (x, y) not in monsters:
        return "None", "None"
    return monsters[x, y].name, monsters[x, y].text


def addmon(name, text, hp, x, y):
    flag = (x, y) in monsters
    monsters[x, y] = Monster(name, text, hp)
    return str(flag)[0]


def serve(conn: socket.socket, addr):
    print(f"Connected with {addr[0]}:{addr[1]}")
    with conn:
        while data := conn.recv(1024):
            match shlex.split(data.decode()):
                case ["move", dx, dy]:
                    conn.sendall(
                        shlex.join(p1.move(int(dx), int(dy))).encode()
                    )
                case ["addmon", name, text, hp, x, y]:
                    conn.sendall(addmon(
                        name, text, int(hp), int(x), int(y)
                    ).encode())
                case ["attack", name, damage]:
                    conn.sendall(
                        shlex.join(p1.attack(name, int(damage))).encode()
                    )
    print(f"Disconnected from {addr[0]}:{addr[1]}")


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
    sockfd.bind((host, port))
    sockfd.listen()
    serve(*sockfd.accept())
