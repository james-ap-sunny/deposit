"""
Logging configuration for the banking application
"""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(app):
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(app.config.get('LOG_FILE', '/app/logs/banking.log'))
    os.makedirs(log_dir, exist_ok=True)
    
    # Set log level
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper())
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        app.config.get('LOG_FILE', '/app/logs/banking.log'),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Configure Flask app logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    
    # Configure SQLAlchemy logging (reduce verbosity in production)
    if not app.config.get('DEBUG', False):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
    
    app.logger.info("Logging configured successfully")


def log_transaction(transfer_id, action, details=None, level='INFO'):
    """Log transaction-specific events"""
    logger = logging.getLogger('transaction')
    
    message = f"Transfer {transfer_id}: {action}"
    if details:
        message += f" - {details}"
    
    if level.upper() == 'ERROR':
        logger.error(message)
    elif level.upper() == 'WARNING':
        logger.warning(message)
    elif level.upper() == 'DEBUG':
        logger.debug(message)
    else:
        logger.info(message)


def log_audit(user_id, action, resource, details=None):
    """Log audit events"""
    audit_logger = logging.getLogger('audit')
    
    audit_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'action': action,
        'resource': resource,
        'details': details or {}
    }
    
    audit_logger.info(f"AUDIT: {audit_entry}")


class TransactionLogger:
    """Context manager for transaction logging"""
    
    def __init__(self, transfer_id, operation):
        self.transfer_id = transfer_id
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.utcnow()
        log_transaction(self.transfer_id, f"{self.operation} started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.utcnow() - self.start_time).total_seconds()
        
        if exc_type is None:
            log_transaction(
                self.transfer_id, 
                f"{self.operation} completed successfully",
                f"Duration: {duration:.3f}s"
            )
        else:
            log_transaction(
                self.transfer_id,
                f"{self.operation} failed",
                f"Error: {str(exc_val)}, Duration: {duration:.3f}s",
                level='ERROR'
            )