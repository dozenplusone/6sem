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


def movePlayer(player: Player, dir: str):
    player.move(dir)
    if (player.x, player.y) in monsters:
        encounter(player.x, player.y)


def parse_addmon(args: list[str]):
    assert len(args) > 7 and all(w in args for w in ("hello", "hp", "coords"))
    arg = {"name": args[0]}
    i = 1
    while i < len(args):
        if args[i] == "hello":
            arg["text"] = args[i + 1]
            i += 1
        elif args[i] == "hp":
            arg["hp"] = int(args[i + 1])
            i += 1
        elif args[i] == "coords":
            x_y = int(args[i + 1]), int(args[i + 2])
            assert 0 <= x_y[0] <= 9 and 0 <= x_y[1] <= 9
            i += 2
        i += 1
    return x_y, arg


def runCmd(cmd: str):
    try:
        cmd = shlex.split(cmd)
    except ValueError:
        print("Invalid arguments")
        return
    match cmd:
        case ["up" | "down" | "left" | "right", *args]:
            assert not args, "Invalid arguments"
            movePlayer(p1, cmd[0])
        case ["addmon", *args]:
            try:
                p, arg = parse_addmon(args)
            except Exception:
                print("Invalid arguments")
                return
            flag = p in monsters
            monsters[p] = Monster(**arg)
            print("Added monster", arg["name"], f"(hp={arg['hp']}) to", p,
                  "saying", arg["text"])
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