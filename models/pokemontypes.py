"""
Description: Junction table for many-to-many relationship between Pokemon and Types.
Author: Bryan Vela
Created: 2026-01-29 - File created and model implementation.
"""
from sqlalchemy import Table, Column, Integer, ForeignKey
from utils.db import db

# junction table for many-to-many: Pokemon / Types
pokemon_types = Table(
    'pokemon_types',
    db.Model.metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemon.id', ondelete='CASCADE'), primary_key=True),
    Column('type_id', Integer, ForeignKey('pokemon_type.id', ondelete='CASCADE'), primary_key=True),
    Column('slot', Integer, nullable=False, default=1)  # to indicate primary/secondary type
)
