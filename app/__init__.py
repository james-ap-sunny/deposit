"""
Core Banking Transfer Transaction System
Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
import os
from datetime import timedelta

from app.config.settings import Config
from app.database.connection import init_databases
from app.utils.logger import setup_logging


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Store the config object for accessing properties
    app.config['CONFIG_OBJECT'] = config_class
"""
Core Banking Transfer Transaction System
Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
import os
from datetime import timedelta

from app.config.settings import Config
from app.database.connection import init_databases
from app.utils.logger import setup_logging


def create_app(config_class=Config):
"""
Core Banking Transfer Transaction System
Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
import os
from datetime import timedelta

from app.config.settings import Config
from app.database.connection import init_databases
from app.utils.logger import setup_logging


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    CORS(app)
    
    # JWT Configuration
    jwt = JWTManager(app)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize databases
    init_databases(app)
    
    # Register blueprints
    from app.api.health_api import health_bp
    from app.api.account_api import account_bp
    from app.api.transfer_api import transfer_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(account_bp, url_prefix='/api/v1')
    app.register_blueprint(transfer_bp, url_prefix='/api/v1')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
    
    app.logger.info('Banking application initialized successfully')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)