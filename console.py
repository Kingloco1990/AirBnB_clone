#!/usr/bin/python3
""" This module defines a command interpreter class for the Airbnb clone
    project.
"""
import cmd
import shlex
from models.base_model import BaseModel
import models


def parse(line):
    """Parses an input string, and returns a list of tokens
       based on shell-like syntax.
    """
    return shlex.split(line)


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand is a command-line interpreter class for the
    Airbnb clone project.

    Attributes:
        prompt (str): The prompt displayed for user input.

    Methods:
        do_quit(self, arg): Exit the command interpreter.
        do_EOF(self, arg): Handle the EOF signal to exit the program.
        do_count(self, line): Count the number of words in a given line.
        do_create(self, line): Create a new instance of BaseModel,
                               save it to the JSON file, and print its id.
        do_show(self, line): Print the string representation of an instance
                             based on the class name and id.
        do_destroy(self, line): Delete an instance based on the
                                class name and id.
        do_all(self, line): Print string representations of all instances
                            based on the class name or all instances.
        do_update(self, line): Update an instance based on the class name and
                               id by adding or updating an attribute.
    """
    prompt = "(hbnb) "
    classes = ['BaseModel']

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print()
        return True

    def do_create(self, line):
        """
        Create a new instance of BaseModel, save it to the JSON file,
        and print its id.

        Usage: create <class> or
               create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        """
        args = parse(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            obj = eval("{}()".format(args[0]))
            print(obj.id)
            models.storage.save()

    def do_show(self, line):
        """
        Prints the string representation of an instance based
        on the class name and id.

        Usage: show <class> <id>
        """
        args = parse(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance is missing **")
        else:
            objs = models.storage.all()
            key = '{}.{}'.format(args[0], args[1])
            try:
                obj = objs[key]
                print(obj)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id.

        Usage: destroy <class> <id>
        """
        args = parse(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objs = models.storage.all()
            key = '{}.{}'.format(args[0], args[1])
            try:
                obj = objs[key]
                objs.pop(key)
                del obj
                models.storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        """
        Prints all string representation of all instances based on the
        class name. When class name is not specified, it prints all
        instantiated objects.

        Usage: all <class> or all
        """
        objs = models.storage.all()
        args = parse(line)
        obj_list = []
        if len(args) >= 1:
            if args[0] not in self.classes:
                print("** class doesn't exist **")
            else:
                for key, obj in objs.items():
                    if key.startswith(args[0]):
                        obj_list.append(obj.__str__())
                print(obj_list)
        else:
            for obj in objs.values():
                obj_list.append(obj.__str__())
            print(obj_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding
        or updating an attribute.

        usage: <class name> <id> <attribute name> "<attribute value>"
        """
        objs = models.storage.all()
        args = parse(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = '{}.{}'.format(args[0], args[1])
            try:
                obj = objs[key]
                if len(args) == 2:
                    print("** attribute name missing **")
                elif len(args) == 3:
                    print("** value missing **")
                else:
                    try:
                        # Convert the attribute (fourth argument) value to
                        # the appropriate data type
                        eval(args[3])
                    except (SyntaxError, NameError):
                        args[3] = "'{}'".format(args[3])
                    setattr(obj, args[2], eval(args[3]))
                    obj.save()
            except KeyError:
                print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
