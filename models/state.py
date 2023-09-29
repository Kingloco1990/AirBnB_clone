#!/usr/bin/python3
"""This module defines the State class, which inherits from BaseModel
"""
from models.base_model import BaseModel


class State(BaseModel):
    """
    Represent a state.

    Args:
        BaseModel (class): The base class for all models.

    Attributes:
        name (str): The name of the state.
    """
    name = ""
