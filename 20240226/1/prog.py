import cowsay
import sys


x, y = 0, 0

while cmd := sys.stdin.readline():
    match cmd.strip():
        case "up":
            y -= 1
        case "down":
            y += 1
        case "left":
            x -= 1
        case "right":
            x += 1
