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
    """
    curly_braces = re.search(r"\{(.*?)\}", line)
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
            return False
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in objs_dict.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args) == 4:
            obj = objs_dict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = value_type(args[3])
            else:
                obj.__dict__[args[2]] = args[3]

        elif type(eval(args[2])) == dict:
            obj = objs_dict["{}.{}".format(args[0], args[1])]
            for key, value in eval(args[2]).items():
                if (
                    key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}
                        ):
                    value_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = value_type(value)
                else:
                    obj.__dict__[key] = value
        models.storage.save()

    def do_count(self, line):
        """
        Retrieves the number of instances of a given class.

        Usage: <class name>.count()
        """
        objs_dict = models.storage.all()
        args = parse(line)
        count = 0
        for obj in objs_dict.values():
            if args[0] == obj.__class__.__name__:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
