#!/usr/bin/python3
""" This module defines a command interpreter class for the HBNB project.
"""
import cmd


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand is a command-line interpreter class for the
    Airbnb clone project.

    Attributes:
        prompt (str): The prompt displayed for user input.

    Methods:
        do_quit(self, arg): Exit the command interpreter.
        do_EOF(self, arg): Handle the EOF signal to exit the program.
    """
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print()
        return True

    def emptyline(self):
        """Override the default behavior for empty input lines"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
