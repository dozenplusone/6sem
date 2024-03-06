import cowsay
import sys


class Player:
    def __init__(self, x: int = 0, y: int = 0):
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


def encounter(x, y):
    name, text = monsters[x, y]
    print(cowsay.cowsay(text, cow=name))


x, y = 0, 0
monsters = {}

while cmd := sys.stdin.readline().split():
    match cmd:
        case ["up" | "down" | "left" | "right", *args]:
            if len(args) > 0:
                print("Invalid arguments")
                continue
            if cmd[0] == "up":
                y = y - 1 if y > 0 else 9
            elif cmd[0] == "down":
                y = y + 1 if y < 9 else 0
            elif cmd[0] == "left":
                x = x - 1 if x > 0 else 9
            elif cmd[0] == "right":
                x = x + 1 if x < 9 else 0
            p = x, y
            print("Moved to", p)
            if p in monsters:
                encounter(*p)
        case ["addmon", *args]:
            try:
                _x, _y = int(args[1]), int(args[2])
                name, hello = args[0], args[3]
                assert 0 <= _x <= 9 and 0 <= _y <= 9
            except Exception:
                print("Invalid arguments")
                continue
            if name not in cowsay.list_cows():
                print("Cannot add unknown monster")
                continue
            p = _x, _y
            flag = p in monsters
            monsters[p] = name, hello
            print("Added monster", name, "to", p, "saying", hello)
            if flag:
                print("Replaced the old monster")
        case _:
            print("Invalid command")
