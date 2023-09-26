#!/usr/bin/python3
"""
__init__ magic method for the models directory.

This module initializes the FileStorage instance for the models directory and
performs an initial reload of stored data.
"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
