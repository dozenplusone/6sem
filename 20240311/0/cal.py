import calendar
import cmd


class CalShell(cmd.Cmd):
    """A simple shell for calendar.TextCalendar."""
    prompt = "$ "
    __runner = calendar.TextCalendar()
    __months = {m.name: m.value for m in calendar.Month}

    def do_prmonth(self, arg):
        """Print a month's calendar as returned by formatmonth()."""
        y, m = arg.split()
        self.__class__.__runner.prmonth(int(y), self.__class__.__months[m])

    def complete_prmonth(self, text, line, begidx, endidx):
        return [m for m in self.__class__.__months if m.startswith(text)]

    def do_pryear(self, arg):
        """Print the calendar for an entire year as returned by formatyear()."""
        self.__class__.__runner.pryear(int(arg))

    def do_EOF(self, arg):
        print()
        return True

    def emptyline(self):
        pass


if __name__ == "__main__":
    CalShell().cmdloop()
