#!/usr/bin/python3
"""This module defines the User class, a subclass of BaseModel.
"""
from models.base_model import BaseModel


class User(BaseModel):
    """User class represents users in the application.

    Args:
        BaseModel (class): The base class for all models.

    Attributes:
              email (str): The user's email address.
              password (str): The user's password.
              first_name (str): The user's first name.
              last_name (str): The user's last name.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
