"""
Description: Abstract base model for all database tables using SQLAlchemy.
Author: Bryan Vela
Created: 2026-01-29 - File created and model implementation.
"""
from .base_model import BaseModel
from utils.db import db

class Pokemon(BaseModel):