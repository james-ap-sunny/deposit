#!/bin/bash
# Script to fix the database connection issue in the banking app

echo "=== Banking App Database Connection Fix ==="

# Create a backup of the original files
echo "Creating backups of original files..."
docker exec banking-app cp /app/app/database/connection.py /app/app/database/connection.py.bak
docker exec banking-app cp /app/app/config/settings.py /app/app/config/settings.py.bak

# Fix the settings.py file to use string URIs instead of properties
echo "Fixing settings.py..."
cat << 'EOF' > settings.py.new
"""
Configuration settings for the banking application
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database Configuration - Source Database
    DB1_HOST = os.environ.get('DB1_HOST') or 'localhost'
    DB1_PORT = int(os.environ.get('DB1_PORT') or 3306)
    DB1_NAME = os.environ.get('DB1_NAME') or 'bank_source'
    DB1_USER = os.environ.get('DB1_USER') or 'bank_user'
    DB1_PASSWORD = os.environ.get('DB1_PASSWORD') or 'secure_password123'
    
    # Database Configuration - Destination Database
    DB2_HOST = os.environ.get('DB2_HOST') or 'localhost'
    DB2_PORT = int(os.environ.get('DB2_PORT') or 3307)
    DB2_NAME = os.environ.get('DB2_NAME') or 'bank_dest'
    DB2_USER = os.environ.get('DB2_USER') or 'bank_user'
    DB2_PASSWORD = os.environ.get('DB2_PASSWORD') or 'secure_password123'
    
    # Redis Configuration
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or None
    
    # Business Rules Configuration
    MAX_TRANSFER_AMOUNT = float(os.environ.get('MAX_TRANSFER_AMOUNT') or 50000.00)
    DAILY_TRANSFER_LIMIT = float(os.environ.get('DAILY_TRANSFER_LIMIT') or 100000.00)
    MIN_TRANSFER_AMOUNT = float(os.environ.get('MIN_TRANSFER_AMOUNT') or 0.01)
    TRANSACTION_TIMEOUT = int(os.environ.get('TRANSACTION_TIMEOUT') or 30)
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or '/app/logs/banking.log'
    
    # Database Connection Pool Settings
    DB_POOL_SIZE = int(os.environ.get('DB_POOL_SIZE') or 10)
    DB_POOL_TIMEOUT = int(os.environ.get('DB_POOL_TIMEOUT') or 30)
    DB_POOL_RECYCLE = int(os.environ.get('DB_POOL_RECYCLE') or 3600)
    
    # Database URIs as string properties (not methods)
    SOURCE_DATABASE_URI = f"mysql+pymysql://{DB1_USER}:{DB1_PASSWORD}@{DB1_HOST}:{DB1_PORT}/{DB1_NAME}?charset=utf8mb4"
    DEST_DATABASE_URI = f"mysql+pymysql://{DB2_USER}:{DB2_PASSWORD}@{DB2_HOST}:{DB2_PORT}/{DB2_NAME}?charset=utf8mb4"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    def __init__(self):
        # Update database URIs with instance variables
        self.SOURCE_DATABASE_URI = f"mysql+pymysql://{self.DB1_USER}:{self.DB1_PASSWORD}@{self.DB1_HOST}:{self.DB1_PORT}/{self.DB1_NAME}?charset=utf8mb4"
        self.DEST_DATABASE_URI = f"mysql+pymysql://{self.DB2_USER}:{self.DB2_PASSWORD}@{self.DB2_HOST}:{self.DB2_PORT}/{self.DB2_NAME}?charset=utf8mb4"


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    
    def __init__(self):
        # Update database URIs with instance variables
        self.SOURCE_DATABASE_URI = f"mysql+pymysql://{self.DB1_USER}:{self.DB1_PASSWORD}@{self.DB1_HOST}:{self.DB1_PORT}/{self.DB1_NAME}?charset=utf8mb4"
        self.DEST_DATABASE_URI = f"mysql+pymysql://{self.DB2_USER}:{self.DB2_PASSWORD}@{self.DB2_HOST}:{self.DB2_PORT}/{self.DB2_NAME}?charset=utf8mb4"


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    def __init__(self):
        # Update database URIs with instance variables
        self.SOURCE_DATABASE_URI = f"mysql+pymysql://{self.DB1_USER}:{self.DB1_PASSWORD}@{self.DB1_HOST}:{self.DB1_PORT}/{self.DB1_NAME}?charset=utf8mb4"
        self.DEST_DATABASE_URI = f"mysql+pymysql://{self.DB2_USER}:{self.DB2_PASSWORD}@{self.DB2_HOST}:{self.DB2_PORT}/{self.DB2_NAME}?charset=utf8mb4"


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
EOF

# Copy the new settings file to the container
docker cp settings.py.new banking-app:/app/app/config/settings.py

# Fix the app.py file
echo "Fixing app.py..."
cat << 'EOF' > app.py.new
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
EOF

# Copy the new app.py file to the container
docker cp app.py.new banking-app:/app/app.py

# Restart the container
echo "Restarting the banking-app container..."
docker-compose restart banking-app

# Check the status
echo "Checking container status..."
docker-compose ps

echo "Fix applied. Check the logs to see if the issue is resolved:"
echo "docker-compose logs banking-app"