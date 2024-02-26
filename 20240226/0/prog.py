import cowsay
import sys


if sys.argv[1] in cowsay.list_cows():
    print(cowsay.cowsay(' '.join(sys.argv[2:]), sys.argv[1]))
else:
    with open(sys.argv[1]) as f:
        cowfile = cowsay.read_dot_cow(f)
    print(cowsay.cowsay(' '.join(sys.argv[2:]), cowfile=cowfile))
