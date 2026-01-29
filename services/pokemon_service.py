"""
Description: Pokemon logic service.
Author: Bryan Vela
Created: 2026-01-29
"""
from typing import List, Optional, Dict, Any
from models.pokemon import Pokemon
from models.pokemonType import PokemonType
from models.pokemonStat import PokemonStat
from models.pokemonAbility import PokemonAbility
from utils.db import db
from services.pokeapi_service import PokeAPIService, PokeAPITransformer
from services.validators import InputValidator, DataValidator


class PokemonService:
    """Pokemon business logic."""
    
    def __init__(self):
        self.api_service = PokeAPIService()
        self.transformer = PokeAPITransformer()
    
    def get_all_pokemon(self, limit: int = 100) -> List[Pokemon]: #limit 100 pokemon
        """Get all Pokemon from database."""
        return Pokemon.query.limit(limit).all()
    
    def get_pokemon_by_id(self, pokemon_id: int) -> Optional[Pokemon]:
        """Get Pokemon by ID."""
        return Pokemon.get_by_id(pokemon_id)
    
    def get_pokemon_by_name(self, name: str) -> Optional[Pokemon]:
        """Get Pokemon by name (case-insensitive)."""
        return Pokemon.query.filter(Pokemon.name.ilike(name)).first()
    
    def fetch_and_save_pokemon(self, pokemon_name: str) -> Optional[Pokemon]:
        """
        Fetch from PokeAPI and save to database.
        
        Steps:
        1. Sanitize input
        2. Check if exists
        3. Fetch from API
        4. Transform data
        5. Validate data
        6. Save to DB
        """
        # s 1: Sanitize
        sanitized = InputValidator.sanitize_name(pokemon_name)
        if not sanitized:
            print(f"invalid name format: {pokemon_name}")
            return None
        
        # s 2: Check if exists
        existing = self.get_pokemon_by_name(sanitized)
        if existing:
            print(f"{sanitized} already exists (ID: {existing.id})")
            return existing
        
        # s 3: Fetch from API
        print(f"Fetching {sanitized} from PokeAPI...")
        api_data = self.api_service.get_pokemon(sanitized)
        if not api_data:
            print(f"failed to fetch {sanitized}")
            return None
        
        # s 4: Transform 
        transformed = self.transformer.transform_pokemon(api_data)
        if not transformed:
            print(f"Failed to transform {sanitized}")
            return None
        
        #s 5: Validate
        is_valid, errors = DataValidator.validate_pokemon_data(transformed)
        if not is_valid:
            print(f"❌ Validation failed for {sanitized}:")
            for error in errors:
                print(f"   - {error}")
            return None
        
        # Step 6: Save
        try:
            pokemon = self._save_pokemon_with_relations(transformed)
            print(f"saved {sanitized} (ID: {pokemon.id})")
            return pokemon
        except Exception as e:
            print(f"save error: {str(e)}")
            db.session.rollback()
            return None
    
    def _save_pokemon_with_relations(self, data: Dict[str, Any]) -> Pokemon:
        """Save Pokemon with types, stats, and abilities."""
        # Create Pokemon
        pokemon = Pokemon(
            name=data['name'],
            pokedex_number=data['pokedex_number'],
            height=data['height'],
            weight=data['weight'],
            sprite_front_default=data.get('sprite_front_default'),
            sprite_front_shiny=data.get('sprite_front_shiny')
        )
        db.session.add(pokemon)
        db.session.flush()  # Get ID
        
        # Add types (many-to-many)
        for type_data in data.get('types', []):
            pokemon_type = PokemonType.get_or_create(type_data['name'])
            pokemon.types.append(pokemon_type)
        
        # Add stats (one-to-many)
        for stat_data in data.get('stats', []):
            stat = PokemonStat(
                pokemon_id=pokemon.id,
                name=stat_data['name'],
                value=stat_data['value']
            )
            db.session.add(stat)
        
        # Add abilities (one-to-many)
        for ability_data in data.get('abilities', []):
            ability = PokemonAbility(
                pokemon_id=pokemon.id,
                name=ability_data['name'],
                is_hidden=1 if ability_data['is_hidden'] else 0,
                slot=ability_data['slot']
            )
            db.session.add(ability)
        
        db.session.commit()
        return pokemon
    
    def sync_pokemon_list(self, pokemon_names: List[str]) -> Dict[str, Any]:
        """
        Sync multiple Pokemon from PokeAPI.

        """
        results = {
            'success': [],
            'failed': [],
            'already_exists': [],
            'total': len(pokemon_names)
        }
        
        for name in pokemon_names:
            name = name.strip()
            
            if self.get_pokemon_by_name(name):
                results['already_exists'].append(name)
                continue
            
            pokemon = self.fetch_and_save_pokemon(name)
            if pokemon:
                results['success'].append(name)
            else:
                results['failed'].append(name)
        
        return results