import cmd
import cowsay
import shlex
from custom import custom


class Player:
    def __init__(self, x: int = 0, y: int = 0):
        assert 0 <= x <= 9 and 0 <= y <= 9, "Invalid initial position"
        self.x, self.y = x, y

    def move(self, dx, dy):
        self.x = (self.x + dx) % 10
        self.y = (self.y + dy) % 10
        print("Moved to", (self.x, self.y))
        encounter(self.x, self.y)

    def attack(self, name, weapon):
        if ((self.x, self.y) not in monsters
                or monsters[self.x, self.y].name != name):
            print(f"No {name} here")
            return
        damage = min(monsters[self.x, self.y].hp, weapons[weapon])
        monsters[self.x, self.y].hp -= damage
        print(f"Attacked {monsters[self.x, self.y].name}, damage {damage} hp")
        if monsters[self.x, self.y].hp > 0:
            print(f"{monsters[self.x, self.y].name} now has",
                  monsters[self.x, self.y].hp)
        else:
            print(monsters[self.x, self.y].name, "died")
            del monsters[self.x, self.y]


p1 = Player()


class Monster:
    def __init__(self, name: str, text: str, hp: int):
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
    assert len(args) > 7 \
        and all(w in args for w in ("hello", "hp", "coords")), \
        "Invalid arguments"
    assert args[0] in cowsay.list_cows() or args[0] in custom, \
        "Cannot add unknown monster"
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


weapons = {"sword": 10, "spear": 15, "axe": 20}


def parse_attack(args: list[str]):
    assert len(args) > 0 and len(args) != 2, "Invalid arguments"
    ans = {"weapon": "sword", "name": args[0]}
    if len(args) > 2 and "with" == args[1]:
        assert args[2] in weapons, "Unknown weapon"
        ans["weapon"] = args[2]
    return ans


class CliRunner(cmd.Cmd):
    prompt = ''
    availables = list(custom) + cowsay.list_cows()

    def do_EOF(self, arg):
        print()
        return True

    def do_up(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.move(0, -1)

    def do_down(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.move(0, 1)

    def do_left(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.move(-1, 0)

    def do_right(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            p1.move(1, 0)

    def do_addmon(self, arg):
        try:
            coords, args = parse_addmon(shlex.split(arg))
        except AssertionError as err:
            print(err)
        else:
            addmon(coords, args)

    def do_attack(self, arg):
        try:
            args = parse_attack(shlex.split(arg))
        except Exception as exc:
            print(exc)
        else:
            p1.attack(**args)

    def complete_attack(self, text, line, begidx, endidx):
        last = shlex.split(line)[-2 if text else -1]
        if last == "with":
            return [w for w in weapons if w.startswith(text)]
        elif last == "attack":
            return [m for m in self.__class__.availables if m.startswith(text)]


if __name__ == "__main__":
    print("<<< Welcome to Python-MUD 0.1 >>>")
    CliRunner().cmdloop()
