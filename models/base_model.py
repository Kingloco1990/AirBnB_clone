#!/usr/bin/python3
"""This module provides a class that defines all common attributes/methods
   for other classes.
"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
    A parent class for common attributes and methods used by other classes.

    Attributes:
        id (str): A unique identifier generated using the UUID version 4.
        created_at (datetime): The date and time when an instance is created.
        updated_at (datetime): The date and time when an instance is last
                               updated.

    Methods:
        __init__(): Initializes a new instance with a unique ID and current
                    timestamps.
        save(): Updates the `updated_at` timestamp to the current date and
                time.
        to_dict(): Converts the object's attributes to a dictionary for
                   serialization.
        __str__(): Returns a string representation of the object.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        - Sets a unique identifier ('id') using UUID version 4.
        - Initializes 'created_at' and 'updated_at' with the
          current date and time.

        Args:
            *args: Variable length positional arguments (not used here).
            **kwargs: Variable length keyword arguments that can be provided
                to set specific attribute values, including 'created_at' and
                'updated_at'.
        """
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        value = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f")
                        setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: A string containing the class name, unique ID, and attribute
                 dictionary.
        """
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the 'updated_at' timestamp to the current date and time.

        This method is called whenever an object is updated.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Converts the object's attributes to a dictionary for serialization.

        Returns:
            dict: A dictionary containing the object's attributes and values,
                  suitable for serialization.
        """
        class_name = self.__class__.__name__
        # Creates a separate copy of the object's attributes to avoid modifying
        # the original object unintentionally
        obj_dict = self.__dict__.copy()
        # Adds the 'id', 'created_at' and 'updated_at' attributes to obj_dict
        obj_dict['id'] = self.id
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict['__class__'] = class_name
        return obj_dict
