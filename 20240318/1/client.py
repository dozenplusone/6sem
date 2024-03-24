import cmd
import cowsay
import shlex
import socket
import sys
from custom import custom


def move(x, y, name, text):
    print(f"Moved to ({x}, {y})")
    if name != "None":
        if name in custom:
            print(cowsay.cowsay(text, cowfile=custom[name]))
        else:
            print(cowsay.cowsay(text, cow=name))


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
    ans = {"damage": 10, "name": args[0]}
    if len(args) > 2 and "with" == args[1]:
        assert args[2] in weapons, "Unknown weapon"
        ans["damage"] = weapons[args[2]]
    return ans


class CliRunner(cmd.Cmd):
    prompt = ''
    availables = list(custom) + cowsay.list_cows()

    def __init__(self, sockfd: socket.socket):
        super().__init__()
        self.sockfd = sockfd

    def do_EOF(self, arg):
        print()
        return True

    def do_up(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            self.sockfd.sendall(b"move 0 -1")
            move(*shlex.split(self.sockfd.recv(1024).decode()))

    def do_down(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            self.sockfd.sendall(b"move 0 1")
            move(*shlex.split(self.sockfd.recv(1024).decode()))

    def do_left(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            self.sockfd.sendall(b"move -1 0")
            move(*shlex.split(self.sockfd.recv(1024).decode()))

    def do_right(self, arg):
        if arg:
            print("Invalid arguments")
        else:
            self.sockfd.sendall(b"move 1 0")
            move(*shlex.split(self.sockfd.recv(1024).decode()))

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


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

if __name__ == "__main__":
    print("<<< Welcome to Python-MUD 0.1 >>>")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
        sockfd.connect((host, port))
        CliRunner(sockfd).cmdloop()
