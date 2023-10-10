#!/usr/bin/python3
"""This module defines the City class, which inherits from BaseModel.
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    City class for representing cities.

    Args:
         BaseModel (class): The base class for all models.

    Attributes:
              state_id (str): The ID of the state associated with the city.
              name (str): The name of the city.
    """
    state_id = ""
    name = ""
