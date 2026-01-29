"""
Description: Pokemon Type model (example: Fire, Water, Grass).
Author: Bryan Vela
Created: 2026-01-29 - File created and model implementation.
"""
from .base_model import BaseModel
from utils.db import db
from .pokemontypes import pokemon_types

class PokemonType(BaseModel):
    __tablename__ = 'pokemon_type'
    
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Relationship
    pokemon = db.relationship(
        'Pokemon',
        secondary=pokemon_types,
        back_populates='types'
    )
    
    def to_dict(self):
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name
        })
        return base_dict
    
    @classmethod
    def get_by_name(cls, name):
        """Get type by name"""
        return cls.query.filter(cls.name.ilike(name)).first()
    
    @classmethod
    def get_or_create(cls, name):
        """
        Get existing type or create new one.
        
        Args:
            name (str): Type name
            
        Returns:
            PokemonType: Existing or new type
        """
        type_obj = cls.get_by_name(name)
        if not type_obj:
            type_obj = cls.create({'name': name.lower()})
        return type_obj