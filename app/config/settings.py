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
    
    @property
    def SOURCE_DATABASE_URI(self):
        """Source database connection URI"""
        return f"mysql+pymysql://{self.DB1_USER}:{self.DB1_PASSWORD}@{self.DB1_HOST}:{self.DB1_PORT}/{self.DB1_NAME}?charset=utf8mb4"
    
    @property
    def DEST_DATABASE_URI(self):
        """Destination database connection URI"""
        return f"mysql+pymysql://{self.DB2_USER}:{self.DB2_PASSWORD}@{self.DB2_HOST}:{self.DB2_PORT}/{self.DB2_NAME}?charset=utf8mb4"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}