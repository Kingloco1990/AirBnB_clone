#!/usr/bin/python3
""" This module defines a command interpreter class for the Airbnb clone
    project.
"""
import cmd
import shlex
import re
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(line):
    """Parses an input string, and returns a list of tokens
       based on shell-like syntax.

    Args:
        line (str): The input string to be parsed.

    Returns:
        list: A list of parsed tokens.
    """
    curly_braces = re.search(r"\{(.*?)\}", line)
    square_brackets = re.search(r"\[(.*?)\]", line)
    if curly_braces is None:
        return [i.strip(",") for i in shlex.split(line)]
    else:
        token_list = shlex.split(line[:curly_braces.span()[0]])
        cleaned_tokens = [i.strip(",") for i in token_list]
        cleaned_tokens.append(curly_braces.group())
        return cleaned_tokens


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand is a command-line interpreter class for the
    Airbnb clone project.

    Attributes:
        prompt (str): The prompt displayed for user input.

    Methods:
        do_quit(self, arg): Exit the command interpreter.
        do_EOF(self, arg): Handle the EOF signal to exit the program.
        do_create(self, line): Create a new instance of BaseModel,
                               save it to the JSON file, and print its id.
        do_show(self, line): Print the string representation of an instance
                             based on the class name and id.
        do_destroy(self, line): Delete an instance based on the class name and
                                id.
        do_all(self, line): Print string representations of all instances
                            based on the class name or all instances.
        do_update(self, line): Update an instance based on the class name and
                               id by adding or updating an attribute.
        do_count(self, line): Count the number of words in a given line.
    """
    prompt = "(hbnb) "
    classes = [
        'BaseModel',
        'User',
        'Place',
        'State',
        'City',
        'Amenity',
        'Review'
        ]

    def default(self, line):
        """
        Handle input that doesn't match any explicit command pattern.

        Args:
            line (str): The input line provided by the user.

        Returns:
            bool: False if the input doesn't match any known command pattern,
            otherwise, it returns the result of executing the recognized
            command.
        """
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            arg = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg[1])
            if match is not None:
                command = [arg[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(arg[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print()
        return True

    def emptyline(self):
        """
        Overrides the default behavior for an empty line.
        In the command interpreter, this ensures that no command is
        executed when an empty line is entered.
        """
        pass

    def do_create(self, line):
        """
        Create a new instance of BaseModel, save it to the JSON file,
        and print its id.
        
        Args:
            line (str): The input line provided by the user.

        Usage: create <class name> or
               create <class name> <key 1>=<value 2> <key 2>=<value 2> ...
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

        Args:
            line (str): The input line provided by the user.

        Usage: show <class name> <id> or <class name>.show(<id>)
        """
        args = parse(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objs_dict = models.storage.all()
            key = '{}.{}'.format(args[0], args[1])
            try:
                obj = objs_dict[key]
                print(obj)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id.

        Args:
            line (str): The input line provided by the user.

        Usage: destroy <class name> <id> or <class name>.destroy(<id>)
        """
        args = parse(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objs_dict = models.storage.all()
            key = '{}.{}'.format(args[0], args[1])
            try:
                obj = objs_dict[key]
                objs_dict.pop(key)
                del obj
                models.storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        """
        Prints all string representation of all instances based on the
        class name. When class name is not specified, it prints all
        instantiated objects.

        Args:
            line (str): The input line provided by the user.

        Usage: all or all <class name> or <class name>.all()
        """
        objs_dict = models.storage.all()
        args = parse(line)
        obj_list = []
        if len(args) > 0:
            if args[0] not in self.classes:
                print("** class doesn't exist **")
            else:
                for key, obj in objs_dict.items():
                    if key.startswith(args[0]):
                        obj_list.append(obj.__str__())
                print(obj_list)
        else:
            for obj in objs_dict.values():
                obj_list.append(obj.__str__())
            print(obj_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding
        or updating an attribute.

        Args:
            line (str): The input line provided by the user.        

        usage: update <class name> <id> <attribute name> "<attribute value>"
               or
               <class name>.update(<id>, <attribute_name>, <attribute_value>)
               or
               <class name>.update(<id>, <dictionary>)
        """
        objs_dict = models.storage.all()
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
                obj = objs_dict[key]
                if len(args) == 2:
                    print("** attribute name missing **")
                elif len(args) == 3:
                    try:
                        result = eval(args[2])
                        if isinstance(result, dict):
                            for k, v in result.items():
                                if k in obj.__dict__.keys():
                                    setattr(obj, k, v)
                                else:
                                    obj.__dict__[k] = v
                            obj.save()
                        else:
                            print("** value missing **")
                    except (SyntaxError, NameError):
                        print("** value missing **")
                else:
                    try:
                        eval(args[3])
                    except (SyntaxError, NameError):
                        args[3] = "'{}'".format(args[3])
                    setattr(obj, args[2], eval(args[3]))
                    obj.save()
            except KeyError:
                print("** no instance found **")

    def do_count(self, line):
        """
        Retrieves the number of instances of a given class.

        Args:
            line (str): The input line provided by the user.

        Usage: <class name>.count()
        """
        objs_dict = models.storage.all()
        args = parse(line)
        count = 0
        for obj in objs_dict.values():
            if args[0] == obj.__class__.__name__:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
