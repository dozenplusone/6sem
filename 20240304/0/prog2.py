import shlex

while (name := input("ФИО = ")) and (place := input("Место = ")):
    print(shlex.join(("register", name, place)))
    print(*shlex.split(input()))
