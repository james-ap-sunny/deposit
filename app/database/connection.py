"""
Database connection management for the banking system
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging

# Global variables for database engines and sessions
source_engine = None
dest_engine = None
SourceSession = None
DestSession = None

logger = logging.getLogger(__name__)


def init_databases(app):
    """Initialize database connections using environment variables directly"""
    global source_engine, dest_engine, SourceSession, DestSession
    
    try:
        # Build source database URI from environment variables
        source_uri = f"mysql+pymysql://{os.getenv('DB1_USER', 'bank_user')}:{os.getenv('DB1_PASSWORD', 'secure_password123')}@{os.getenv('DB1_HOST', 'bank-db1')}:{os.getenv('DB1_PORT', '3306')}/{os.getenv('DB1_NAME', 'bank_source')}?charset=utf8mb4"
        
        # Build destination database URI from environment variables
        dest_uri = f"mysql+pymysql://{os.getenv('DB2_USER', 'bank_user')}:{os.getenv('DB2_PASSWORD', 'secure_password123')}@{os.getenv('DB2_HOST', 'bank-db2')}:{os.getenv('DB2_PORT', '3306')}/{os.getenv('DB2_NAME', 'bank_dest')}?charset=utf8mb4"
        
        logger.info(f"Connecting to source database: {os.getenv('DB1_HOST', 'bank-db1')}:{os.getenv('DB1_PORT', '3306')}/{os.getenv('DB1_NAME', 'bank_source')}")
        logger.info(f"Connecting to destination database: {os.getenv('DB2_HOST', 'bank-db2')}:{os.getenv('DB2_PORT', '3306')}/{os.getenv('DB2_NAME', 'bank_dest')}")
        
        # Source database engine
        source_engine = create_engine(
            source_uri,
            poolclass=QueuePool,
            pool_size=int(os.getenv('DB_POOL_SIZE', '10')),
            pool_timeout=int(os.getenv('DB_POOL_TIMEOUT', '30')),
            pool_recycle=int(os.getenv('DB_POOL_RECYCLE', '3600')),
            pool_pre_ping=True,
            echo=False
        )
        
        # Destination database engine
        dest_engine = create_engine(
            dest_uri,
            poolclass=QueuePool,
            pool_size=int(os.getenv('DB_POOL_SIZE', '10')),
            pool_timeout=int(os.getenv('DB_POOL_TIMEOUT', '30')),
            pool_recycle=int(os.getenv('DB_POOL_RECYCLE', '3600')),
            pool_pre_ping=True,
            echo=False
        )
        
        # Create session factories
        SourceSession = sessionmaker(bind=source_engine)
        DestSession = sessionmaker(bind=dest_engine)
        
        # Test connections
        with source_engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("Source database connection successful")
        
        with dest_engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("Destination database connection successful")
        
        logger.info("Database connections initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize databases: {str(e)}")
        raise


def get_source_session():
    """Get a new source database session"""
    if SourceSession is None:
        raise RuntimeError("Database not initialized")
    return SourceSession()


def get_dest_session():
    """Get a new destination database session"""
    if DestSession is None:
        raise RuntimeError("Database not initialized")
    return DestSession()


def get_source_engine():
    """Get the source database engine"""
    if source_engine is None:
        raise RuntimeError("Database not initialized")
    return source_engine


def get_dest_engine():
    """Get the destination database engine"""
    if dest_engine is None:
        raise RuntimeError("Database not initialized")
    return dest_engine