"""
Description: Input validation and sanitization
Author: Bryan Vela
Created: 2026-01-29
"""
import re
from typing import Optional, Tuple, List


class InputValidator:
    """Validate and sanitize user inputs."""
    
    # Only lowercase letters, numbers, hyphens
    NAME_PATTERN = re.compile(r'^[a-z0-9\-]+$')
    
    @staticmethod
    def sanitize_name(name: str) -> Optional[str]:

        if not name or not isinstance(name, str):
            return None
        
        name = name.strip().lower()
        
        if len(name) < 1 or len(name) > 50:
            return None
        
        if not InputValidator.NAME_PATTERN.match(name):
            return None
        
        return name
    
    @staticmethod
    def sanitize_id(value) -> Optional[int]:
        """
        Sanitize numeric ID.
        
        Returns:
            int: Valid ID (>0) or None
        """
        try:
            value = int(value)
            return value if value > 0 else None
        except (ValueError, TypeError):
            return None


class DataValidator:
    
    @staticmethod
    def validate_pokemon_data(data: dict) -> Tuple[bool, List[str]]:
        """
        Validate Pokemon data structure.
        
        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []
        
        # Required fields
        if not data.get('name'):
            errors.append("Missing name")
        if not data.get('pokedex_number') or data['pokedex_number'] < 1:
            errors.append("Invalid pokedex_number")
        if data.get('height') is None or data['height'] < 0:
            errors.append("Invalid height")
        if data.get('weight') is None or data['weight'] < 0:
            errors.append("Invalid weight")
        
        # Must have at least 1 type, max 2
        types = data.get('types', [])
        if not types:
            errors.append("Must have at least 1 type")
        elif len(types) > 2:
            errors.append("Cannot have more than 2 types")
        
        # Should have 6 stats
        stats = data.get('stats', [])
        if len(stats) != 6:
            errors.append(f"Expected 6 stats, got {len(stats)}")
        
        return (len(errors) == 0, errors)
    