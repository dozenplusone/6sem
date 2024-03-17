import cmd
import cowsay
import shlex
from custom import custom


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
        encounter(self.x, self.y)

    def attack(self):
        pass


p1 = Player()


class Monster:
    def __init__(self, name: str, text: str, hp: int):
        assert name in cowsay.list_cows() or name in custom, \
                "Cannot add unknown monster"
        self.name, self.text, self.hp = name, text, hp


monsters = {}


def encounter(x, y):
    if (x, y) not in monsters:
        return
    monster = monsters[x, y]
    if monster.name in custom:
        print(cowsay.cowsay(monster.text, cowfile=custom[monster.name]))
    else:
        print(cowsay.cowsay(monster.text, cow=monster.name))


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


def addmon(coords, args):
    flag = coords in monsters
    try:
        monsters[coords] = Monster(**args)
    except AssertionError as err:
        print(err)
        return
    print("Added monster", args["name"], f"(hp={args['hp']}) to", coords,
          "saying", args["text"])
    if flag:
        print("Replaced the old monster")


class CliRunner(cmd.Cmd):
    prompt = ''

    def do_EOF(self, arg):
        print()
        return True

    def do_up(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.move("up")

    def do_down(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.move("down")

    def do_left(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.move("left")

    def do_right(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.move("right")

    def do_addmon(self, arg):
        try:
            coords, args = parse_addmon(shlex.split(arg))
        except Exception:
            print("Invalid arguments")
        else:
            addmon(coords, args)

    def do_attack(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.attack()


if __name__ == "__main__":
    print("<<< Welcome to Python-MUD 0.1 >>>")
    CliRunner().cmdloop()

