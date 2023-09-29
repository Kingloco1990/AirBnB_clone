#!/usr/bin/python3
""" This module contains a class with methods that
    serializes a instances to a JSON file and deserializes JSON
    file to instances
"""
import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """
    This class provides methods for serializing instances to a JSON file
    and deserializing JSON files to instances.

    Attributes:
        __file_path (str): The path to the JSON file where data is stored.
        __objects (dict): A dictionary to store serialized objects.

    Methods:
        all(self): Retrieves all serialized objects.
        new(self, obj): Adds a new serialized object to the storage.
        save(self): Serializes and saves objects to the JSON file.
        reload(self): Deserializes objects from the JSON file into storage.
    """
    __file_path = "file.json"  # Default JSON file path
    __objects = {}  # Dictionary to store serialized objects

    def all(self):
        """
        Retrieves/returns all serialized objects.

        Returns:
            dict: A dictionary containing all serialized objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new serialized/deserialized object to storage.

        Args:
            obj (BaseModel): The object to be serialized and added.
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes and saves objects to the JSON file.
        """
        with open(FileStorage.__file_path, 'w', encoding="utf-8") as file:
            obj_dict = {
                key: obj.to_dict()
                for key, obj in FileStorage.__objects.items()
                }
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes objects from the JSON file into storage.
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
