import cowsay
import sys


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
            print("Moved to", (x, y))
        case ["addmon", *args]:
            try:
                _x, _y, hello = int(args[0]), int(args[1]), args[2]
                assert 0 <= _x <= 9 and 0 <= _y <= 9
            except Exception:
                print("Invalid arguments")
                continue
            p = _x, _y
            flag = p in monsters
            monsters[p] = hello
            print("Added monster to", p, "saying", hello)
            if flag:
                print("Replaced the old monster")
        case _:
            print("Invalid command")
