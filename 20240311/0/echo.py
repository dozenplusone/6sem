import cmd


class Shell(cmd.Cmd):
    """A shell with only simple command `echo`."""
    prompt = ":-> "
    __completions = "one", "two", "three", "four", "five"

    def do_echo(self, arg):
        """Echo any string, with any whitespaces."""
        print(arg)

    def complete_echo(self, text, line, begidx, endidx):
        return [c for c in self.__class__.__completions if c.startswith(text)]

    def do_EOF(self, arg):
        print()
        return True

    def emptyline(self):
        pass


if __name__ == "__main__":
    Shell().cmdloop()
