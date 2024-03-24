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
        encounter(self.x, self.y)

    def attack(self, name, damage):
        if ((self.x, self.y) not in monsters
                or monsters[self.x, self.y].name != name):
            print(f"No {name} here")
            return
        damage = min(monsters[self.x, self.y].hp, damage)
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
