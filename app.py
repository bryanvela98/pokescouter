from flask import Flask, jsonify
from config.config import Config
from utils.db import init_db, db

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    #init extension
    init_db(app)
    
    # Register blueprints
    from routes.pokemon_routes import pokemon_bp 
    app.register_blueprint(pokemon_bp, url_prefix='/api/pokemon')
    
#---------routes------------
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy",
                        'message': 'poke scouter is running',
                        }), 200

    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint with API information."""
        return jsonify({
            'name': 'PokeScouter API',
            'description': 'Pokemon scouting and data management API',
            'endpoints': {
                'health': '/health',
                'api_docs': '/api/docs',
                'pokemon': '/api/pokemon'
            }
        }), 200
        
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
        
    return app

if __name__ == '__main__':
    app = create_app()
    print(f"Pokemon List: {app.config['POKEMON_LIST']}")
    app.run(debug=True, host='0.0.0.0', port=5050)