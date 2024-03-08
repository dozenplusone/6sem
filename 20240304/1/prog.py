import cowsay
import shlex
import sys


class Player:
    def __init__(self, x: int = 0, y: int = 0):
        assert 0 <= x <= 9 and 0 <= y <= 9, "Invalid initial position"
        self.x, self.y = x, y

    def move(self, dir: str):
        if dir == "up":
            self.y = self.y - 1 if self.y > 0 else 9
        elif dir == "down":
            self.y = self.y + 1 if self.y < 9 else 0
        elif dir == "left":
            self.x = self.x - 1 if self.x > 0 else 9
        elif dir == "right":
            self.x = self.x + 1 if self.x < 9 else 0
        print("Moved to", (self.x, self.y))


p1 = Player()


class Monster:
    def __init__(self, name: str, text: str, hp: int):
        assert name in cowsay.list_cows() or name == "jgsbat", \
                "Cannot add unknown monster"
        self.name, self.text, self.hp = name, text, hp


monsters = {}


with open("jgsbat.cow") as f:
    jgsbat = cowsay.read_dot_cow(f)


def encounter(x, y):
    monster = monsters[x, y]
    if monster.name == "jgsbat":
        print(cowsay.cowsay(monster.text, cowfile=jgsbat))
    else:
        print(cowsay.cowsay(monster.text, cow=monster.name))


def runCmd(cmd: str):
    try:
        cmd = shlex.split(cmd)
    except ValueError:
        print("Invalid arguments")
        return
    match cmd:
        case ["up" | "down" | "left" | "right", *args]:
            assert not args, "Invalid arguments"
            p1.move(cmd[0])
            if (p1.x, p1.y) in monsters:
                encounter(p1.x, p1.y)
        case ["addmon", *args]:
            assert len(args) > 7 and "coords" in args \
                    and "hp" in args and "hello" in args, "Invalid arguments"
            coords = args.index("coords")
            _x, _y = args[coords + 1: coords + 3]
            hp = args[args.index("hp") + 1]
            try:
                _x, _y, hp = int(_x), int(_y), int(hp)
            except ValueError:
                print("Invalid arguments")
                return
            name, hello = args[0], args[args.index("hello") + 1]
            p = _x, _y
            flag = p in monsters
            monsters[p] = Monster(name, hello, hp)
            print("Added monster", name, f"(hp={hp}) to", p, "saying", hello)
            if flag:
                print("Replaced the old monster")
        case _:
            print("Invalid command")


print("<<< Welcome to Python-MUD 0.1 >>>")

while cmd := sys.stdin.readline():
    try:
        runCmd(cmd)
    except AssertionError as err:
        print(err)
