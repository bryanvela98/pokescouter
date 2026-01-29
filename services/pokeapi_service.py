"""
Description: fetch Pokemon data from PokeAPI.
Author: Bryan Vela
Created: 2026-01-29
"""
import requests
from typing import Optional, Dict, Any
from flask import current_app


class PokeAPIService:
    """Client for PokeAPI."""
    
    def __init__(self):
        self.base_url = current_app.config.get('POKEAPI_BASE_URL')
        self.timeout = current_app.config.get('POKEAPI_TIMEOUT', 10)
    
    def _make_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make GET request to PokeAPI."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Timeout: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP {e.response.status_code}: {url}")
            return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def get_pokemon(self, pokemon_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch Pokemon by name/ID.
        
        Returns PokeAPI response with: name, id, height, weight, 
        types, stats, abilities, sprites
        """
        return self._make_request(f"/pokemon/{pokemon_name.lower()}")


class PokeAPITransformer:
    """Basically this class transforms PokeAPI responses to database format."""
    
    @staticmethod
    def transform_pokemon(api_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Transform PokeAPI response to our DB structure.
    
        """
        if not api_data:
            return None
        
        sprites = api_data.get('sprites', {})
        
        return {
            'name': api_data['name'],
            'pokedex_number': api_data['id'],
            'height': api_data['height'],
            'weight': api_data['weight'],
            'sprite_front_default': sprites.get('front_default'),
            'sprite_front_shiny': sprites.get('front_shiny'),
            'types': [
                {'name': t['type']['name'], 'slot': t['slot']}
                for t in api_data.get('types', [])
            ],
            'stats': [
                {'name': s['stat']['name'], 'value': s['base_stat']}
                for s in api_data.get('stats', [])
            ],
            'abilities': [
                {
                    'name': a['ability']['name'],
                    'is_hidden': a.get('is_hidden', False),
                    'slot': a.get('slot', 1)
                }
                for a in api_data.get('abilities', [])
            ]
        }