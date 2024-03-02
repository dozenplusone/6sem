import cowsay
import sys


x, y = 0, 0

while cmd := sys.stdin.readline():
    match cmd.strip():
        case "up":
            y = y - 1 if y > 0 else 9
        case "down":
            y = y + 1 if y < 9 else 0
        case "left":
            x = x - 1 if x > 0 else 9
        case "right":
            x = x + 1 if x < 9 else 0
