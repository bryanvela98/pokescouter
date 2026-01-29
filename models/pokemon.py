"""
Description: Pokemon model and related tables for Pokemon scouting system.
Author: Bryan Vela
Created: 2026-01-29
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from .pokemontypes import pokemon_types
from utils.db import db

class Pokemon(BaseModel):
    """
    Pokemon model - stores core Pokemon data.
    """
    __tablename__ = 'pokemon'
    
    # Basic Information
    name = db.Column(String(100), unique=True, nullable=False, index=True)
    pokedex_number = db.Column(Integer, unique=True, nullable=False, index=True)
    height = db.Column(Integer, nullable=False)  # in decimetres
    weight = db.Column(Integer, nullable=False)  # in hectograms

    # Sprite URLs
    sprite_front_default = db.Column(String(500), nullable=True)
    sprite_front_shiny = db.Column(String(500), nullable=True)

    # Relationships
    types = db.relationship(
        'PokemonType',
        secondary=pokemon_types,
        back_populates='pokemon',
        lazy='joined'
    )
    stats = db.relationship(
        'PokemonStat',
        back_populates='pokemon',
        cascade='all, delete-orphan',
        lazy='joined'
    )
    abilities = db.relationship(
        'PokemonAbility',
        back_populates='pokemon',
        cascade='all, delete-orphan',
        lazy='joined'
    )
    
    def to_dict(self):
        """
        Convert Pokemon to dictionary with all related data.
        
        Returns:
            dict: Complete Pokemon data
        """
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name,
            'pokedex_number': self.pokedex_number,
            'height': self.height,
            'weight': self.weight,
            'types': [
                {
                    'name': t.name,
                    'slot': self._get_type_slot(t)
                } for t in sorted(self.types, key=lambda x: self._get_type_slot(x))
            ],
            'stats': {stat.name: stat.value for stat in self.stats},
            'abilities': [ability.to_dict() for ability in sorted(self.abilities, key=lambda x: x.slot)],
            'sprites': {
                'front_default': self.sprite_front_default,
                'front_shiny': self.sprite_front_shiny
            }
        })
        return base_dict
    
    def _get_type_slot(self, pokemon_type):
        """Get type slot from association table"""
        result = db.session.execute(
            pokemon_types.select().where(
                (pokemon_types.c.pokemon_id == self.id) & 
                (pokemon_types.c.type_id == pokemon_type.id)
            )
        ).first()
        return result.slot if result else 1
    
    @classmethod
    def get_by_name(cls, name):
        """
        Find Pokemon by name (case-insensitive).
        
        Args:
            name (str): Pokemon name
            
        Returns:
            Pokemon or None: Found Pokemon or None
        """
        return cls.query.filter(cls.name.ilike(name)).first()
    
    @classmethod
    def get_by_pokedex_number(cls, number):
        """
        Find Pokemon by Pokedex number.
        
        Args:
            number (int): Pokedex number
            
        Returns:
            Pokemon or None: Found Pokemon or None
        """
        return cls.query.filter_by(pokedex_number=number).first()
    
    @classmethod
    def exists(cls, name):
        """
        Check if Pokemon exists by name.
        
        Args:
            name (str): Pokemon name
            
        Returns:
            bool: True if exists
        """
        return cls.query.filter(cls.name.ilike(name)).count() > 0
