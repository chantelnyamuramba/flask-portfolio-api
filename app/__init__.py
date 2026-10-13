from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import redis

from app.config import config_by_name

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
redis_client = redis.Redis()


def create_app(config_name='dev'):
    """Application Factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions with app instance
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Initialize Redis connection
    global redis_client
    redis_client = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=0,
        decode_responses=True
    )

    # Health check route
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'environment': config_name
        }), 200

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.items import items_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')

    return app