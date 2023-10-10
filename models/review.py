#!/usr/bin/python3
"""Defines the Review class, inheriting from BaseModel."""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Place class representing a review for a place.

    Args:
        BaseModel (class): The base class for all models.

    Attributes:
        place_id (str): The ID of the place being reviewed.
        user_id (str): The ID of the user who wrote the review.
        text (str): The text content of the review.
    """
    place_id = ""
    user_id = ""
    text = ""
