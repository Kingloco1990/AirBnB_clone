#!/usr/bin/python3
""" This module contains a class with methods that
    serializes a instances to a JSON file and deserializes JSON
    file to instances
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    This module contains a class that provides methods for serializing
    instances to a JSON file and deserializing JSON files to instances.

    Attributes:
        __file_path (str): The path to the JSON file where data is stored.
        __objects (dict): A dictionary to store objects.

    Methods:
        all(self): Returns all objects in storage.
        new(self, obj): Adds a new object to storage.
        save(self): Serializes objects and saves them to the JSON file.
        reload(self): Deserializes string representations saved in the
                      JSON file into objects and then into storage.
    """
    __file_path = "file.json"  # Default JSON file path
    __objects = {}  # Dictionary to store objects

    def all(self):
        """
        Returns all objects in storage.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to storage.

        Args:
            obj (BaseModel): The object to be added.
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes objects and saves them to the JSON file.
        """
        with open(FileStorage.__file_path, 'w', encoding="utf-8") as file:
            obj_dict = {
                key: obj.to_dict()
                for key, obj in FileStorage.__objects.items()
                }
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes string representations saved in the JSON file into
        objects and then into storage.
        """
        try:
            with open(FileStorage.__file_path, 'r', encoding="utf-8") as file:
                json_file = json.load(file)
                for obj in json_file.values():
                    class_name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval('{}({})'.format(class_name, '**obj')))
        except FileNotFoundError:
            pass
