"""
Database connection management for distributed banking system
"""

import logging
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import pymysql

logger = logging.getLogger(__name__)

# Global database engines and session makers
source_engine = None
dest_engine = None
SourceSession = None
DestSession = None


def init_databases(app):
    """Initialize database connections"""
    global source_engine, dest_engine, SourceSession, DestSession
    
    try:
        # Get database connection strings directly from environment variables if not in app.config
        source_db_uri = app.config.get('SOURCE_DATABASE_URI')
        dest_db_uri = app.config.get('DEST_DATABASE_URI')
        
        # If URIs are not available in app.config, build them from environment variables
        if not source_db_uri:
            db1_user = app.config.get('DB1_USER', os.environ.get('DB1_USER', 'bank_user'))
            db1_password = app.config.get('DB1_PASSWORD', os.environ.get('DB1_PASSWORD', 'secure_password123'))
            db1_host = app.config.get('DB1_HOST', os.environ.get('DB1_HOST', 'bank-db1'))
            db1_port = app.config.get('DB1_PORT', os.environ.get('DB1_PORT', '3306'))
            db1_name = app.config.get('DB1_NAME', os.environ.get('DB1_NAME', 'bank_source'))
            source_db_uri = f"mysql+pymysql://{db1_user}:{db1_password}@{db1_host}:{db1_port}/{db1_name}?charset=utf8mb4"
        
        if not dest_db_uri:
            db2_user = app.config.get('DB2_USER', os.environ.get('DB2_USER', 'bank_user'))
            db2_password = app.config.get('DB2_PASSWORD', os.environ.get('DB2_PASSWORD', 'secure_password123'))
            db2_host = app.config.get('DB2_HOST', os.environ.get('DB2_HOST', 'bank-db2'))
            db2_port = app.config.get('DB2_PORT', os.environ.get('DB2_PORT', '3306'))
            db2_name = app.config.get('DB2_NAME', os.environ.get('DB2_NAME', 'bank_dest'))
            dest_db_uri = f"mysql+pymysql://{db2_user}:{db2_password}@{db2_host}:{db2_port}/{db2_name}?charset=utf8mb4"
        
        # Source database engine
        source_engine = create_engine(
            source_db_uri,
            poolclass=QueuePool,
            pool_size=app.config['DB_POOL_SIZE'],
            pool_timeout=app.config['DB_POOL_TIMEOUT'],
            pool_recycle=app.config['DB_POOL_RECYCLE'],
            pool_pre_ping=True,
            echo=app.config.get('DEBUG', False)
        )
        
        # Destination database engine
        dest_engine = create_engine(
            dest_db_uri,
            poolclass=QueuePool,
            pool_size=app.config['DB_POOL_SIZE'],
            pool_timeout=app.config['DB_POOL_TIMEOUT'],
            pool_recycle=app.config['DB_POOL_RECYCLE'],
            pool_pre_ping=True,
            echo=app.config.get('DEBUG', False)
        )
        
        # Session makers
        SourceSession = sessionmaker(bind=source_engine)
        DestSession = sessionmaker(bind=dest_engine)
        
        # Test connections
        test_connections()
        
        logger.info("Database connections initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize databases: {str(e)}")
        raise


def test_connections():
    """Test database connections"""
    try:
        # Test source database
        with source_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        
        # Test destination database
        with dest_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        
        logger.info("Database connection tests passed")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False


@contextmanager
def get_source_session():
    """Get source database session with automatic cleanup"""
    session = SourceSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Source database session error: {str(e)}")
        raise
    finally:
        session.close()


@contextmanager
def get_dest_session():
    """Get destination database session with automatic cleanup"""
    session = DestSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Destination database session error: {str(e)}")
        raise
    finally:
        session.close()


class DatabaseManager:
    """Database manager for distributed transactions"""
    
    def __init__(self):
        self.source_session = None
        self.dest_session = None
        self.transactions_started = False
    
    def begin_distributed_transaction(self):
        """Begin distributed transaction across both databases"""
        try:
            self.source_session = SourceSession()
            self.dest_session = DestSession()
            
            # Begin transactions
            self.source_session.begin()
            self.dest_session.begin()
            
            self.transactions_started = True
            logger.debug("Distributed transaction started")
            
        except Exception as e:
            self.rollback_distributed_transaction()
            logger.error(f"Failed to start distributed transaction: {str(e)}")
            raise
    
    def commit_distributed_transaction(self):
        """Commit distributed transaction (Two-Phase Commit simulation)"""
        if not self.transactions_started:
            raise Exception("No active distributed transaction")
        
        try:
            # Phase 1: Prepare (flush changes but don't commit)
            self.source_session.flush()
            self.dest_session.flush()
            
            # Phase 2: Commit both transactions
            self.source_session.commit()
            self.dest_session.commit()
            
            logger.debug("Distributed transaction committed successfully")
            
        except Exception as e:
            self.rollback_distributed_transaction()
            logger.error(f"Failed to commit distributed transaction: {str(e)}")
            raise
        finally:
            self.cleanup_sessions()
    
    def rollback_distributed_transaction(self):
        """Rollback distributed transaction"""
        try:
            if self.source_session:
                self.source_session.rollback()
            if self.dest_session:
                self.dest_session.rollback()
            
            logger.debug("Distributed transaction rolled back")
            
        except Exception as e:
            logger.error(f"Error during rollback: {str(e)}")
        finally:
            self.cleanup_sessions()
    
    def cleanup_sessions(self):
        """Clean up database sessions"""
        try:
            if self.source_session:
                self.source_session.close()
                self.source_session = None
            
            if self.dest_session:
                self.dest_session.close()
                self.dest_session = None
            
            self.transactions_started = False
            
        except Exception as e:
            logger.error(f"Error during session cleanup: {str(e)}")
    
    def get_source_session(self):
        """Get source database session"""
        if not self.source_session:
            raise Exception("No active source session")
        return self.source_session
    
    def get_dest_session(self):
        """Get destination database session"""
        if not self.dest_session:
            raise Exception("No active destination session")
        return self.dest_session


def get_database_info():
    """Get database connection information for health checks"""
    info = {}
    
    try:
        # Source database info
        with source_engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION() as version, DATABASE() as database"))
            row = result.fetchone()
            info['source'] = {
                'status': 'connected',
                'version': row[0] if row else 'unknown',
                'database': row[1] if row else 'unknown'
            }
    except Exception as e:
        info['source'] = {
            'status': 'error',
            'error': str(e)
        }
    
    try:
        # Destination database info
        with dest_engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION() as version, DATABASE() as database"))
            row = result.fetchone()
            info['dest'] = {
                'status': 'connected',
                'version': row[0] if row else 'unknown',
                'database': row[1] if row else 'unknown'
            }
    except Exception as e:
        info['dest'] = {
            'status': 'error',
            'error': str(e)
        }
    
    return info