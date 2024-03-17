import cowsay


custom = {
    "jgsbat": "jgsbat.cow"
}

for monster in custom:
    with open(custom[monster]) as f:
        custom[monster] = cowsay.read_dot_cow(f)
