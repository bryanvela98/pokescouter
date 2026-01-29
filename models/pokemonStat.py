"""
Description: Pokemon Stats model.
Author: Bryan Vela
Created: 2026-01-29 - File created and model implementation.
"""
from .base_model import BaseModel
from utils.db import db

class PokemonStat(BaseModel):
    """
    Pokemon Stats model (HP, Attack, Defense, etc.).
    """
    __tablename__ = 'pokemon_stat'
    
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id', ondelete='CASCADE'), nullable=False)
    
    # Stat details
    name = db.Column(db.String(50), nullable=False)  # hp, attack, defense, etc.
    value = db.Column(db.Integer, nullable=False)

    # Relationship
    pokemon = db.relationship('Pokemon', back_populates='stats')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'value': self.value
        }