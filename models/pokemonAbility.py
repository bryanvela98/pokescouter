"""
Description: Pokemon Abilities model.
Author: Bryan Vela
Created: 2026-01-29 - File created and model implementation.
"""
from .base_model import BaseModel
from utils.db import db

class PokemonAbility(BaseModel):
    """
    Pokemon Abilities model.
    """
    __tablename__ = 'pokemon_ability'
    
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id', ondelete='CASCADE'), nullable=False)
    
    # Ability details
    name = db.Column(db.String(100), nullable=False)
    is_hidden = db.Column(db.Integer, default=0)  # 0 = normal, 1 = hidden
    slot = db.Column(db.Integer, nullable=False)
    
    # Relationship
    pokemon = db.relationship('Pokemon', back_populates='abilities')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'is_hidden': bool(self.is_hidden),
            'slot': self.slot
        }