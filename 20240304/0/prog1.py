import shlex


while s := shlex.split(input("$ ")):
    try:
        print(shlex.join(s))
    except Exception as exc:
        print(exc)
