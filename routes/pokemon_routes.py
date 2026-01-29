"""
Description: Pokemon REST API routes.
Author: Bryan Vela
Created: 2026-01-29
"""
from flask import Blueprint, jsonify, request
from services.pokemon_service import PokemonService

# Create Blueprint
pokemon_bp = Blueprint('pokemon', __name__)


@pokemon_bp.route('/', methods=['GET'])
def get_all_pokemon():
    """
    Get all Pokemon.
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        limit = min(limit, 500)  # Max 500
        
        service = PokemonService()
        pokemon_list = service.get_all_pokemon(limit=limit)
        
        return jsonify({
            'success': True,
            'count': len(pokemon_list),
            'data': [p.to_dict() for p in pokemon_list]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@pokemon_bp.route('/<int:pokemon_id>', methods=['GET'])
def get_pokemon_by_id(pokemon_id):
    """
    Get Pokemon by ID.
    """
    service = PokemonService()
    pokemon = service.get_pokemon_by_id(pokemon_id)
    
    if not pokemon:
        return jsonify({
            'success': False,
            'error': 'Pokemon not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': pokemon.to_dict()
    }), 200


@pokemon_bp.route('/name/<string:name>', methods=['GET'])
def get_pokemon_by_name(name):
    """
    Get Pokemon by name.
    """
    service = PokemonService()
    pokemon = service.get_pokemon_by_name(name)
    
    if not pokemon:
        return jsonify({
            'success': False,
            'error': f'Pokemon "{name}" not found in database'
        }), 404
    
    return jsonify({
        'success': True,
        'data': pokemon.to_dict()
    }), 200


@pokemon_bp.route('/fetch/<string:name>', methods=['POST'])
def fetch_pokemon(name):
    """
    Fetch Pokemon from PokeAPI and save to database.
    """
    service = PokemonService()
    pokemon = service.fetch_and_save_pokemon(name)
    
    if not pokemon:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch "{name}" from PokeAPI'
        }), 404
    
    return jsonify({
        'success': True,
        'message': f'Pokemon "{pokemon.name}" fetched successfully',
        'data': pokemon.to_dict()
    }), 201


@pokemon_bp.route('/fetch/batch', methods=['POST'])
def fetch_pokemon_batch():
    """
    Fetch multiple Pokemon from PokeAPI.
    """
    data = request.get_json()
    
    if not data or 'pokemon' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing "pokemon" array in request body'
        }), 400
    
    pokemon_list = data['pokemon']
    
    if not isinstance(pokemon_list, list):
        return jsonify({
            'success': False,
            'error': '"pokemon" must be an array'
        }), 400
    
    if len(pokemon_list) == 0:
        return jsonify({
            'success': False,
            'error': 'Pokemon list cannot be empty'
        }), 400
    
    if len(pokemon_list) > 50:
        return jsonify({
            'success': False,
            'error': 'Cannot fetch more than 50 Pokemon at once'
        }), 400
    
    service = PokemonService()
    results = service.sync_pokemon_list(pokemon_list)
    
    return jsonify({
        'success': True,
        'results': results
    }), 200
