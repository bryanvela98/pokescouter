from flask_sqlalchemy import SQLAlchemy

# Singleton database instance
db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        from models.pokemon import Pokemon
        from models.pokemonType import PokemonType
        from models.pokemonStat import PokemonStat
        from models.pokemonAbility import PokemonAbility
        
        # Create all tables
        db.create_all()
        
        print("✅ Database initialized successfully!")


def reset_db(app):
    """Reset database (drop all tables and recreate)"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database reset successfully!")