"""
Main application entry point
"""

from app import create_app
from app.config.settings import config
import os

# Get the environment configuration
env = os.environ.get('FLASK_ENV', 'development')
config_class = config.get(env, config['default'])

# Create Flask application with instantiated config class
app = create_app(config_class())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
