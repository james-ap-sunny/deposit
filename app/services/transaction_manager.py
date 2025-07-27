"""
Distributed transaction manager for handling cross-database transactions
"""

import logging
from app.database.connection import DatabaseManager
from app.utils.exceptions import DistributedTransactionException

logger = logging.getLogger(__name__)


class DistributedTransactionManager(DatabaseManager):
    """
    Enhanced database manager with distributed transaction capabilities
    Implements a simplified two-phase commit protocol
    """
    
    def __init__(self):
        super().__init__()
        self.transaction_id = None
        self.phase = None
    
    def begin_distributed_transaction(self):
        """Begin distributed transaction with enhanced logging"""
        try:
            super().begin_distributed_transaction()
            self.phase = 'STARTED'
            logger.info("Distributed transaction started successfully")
            
        except Exception as e:
            self.phase = 'FAILED'
            logger.error(f"Failed to start distributed transaction: {str(e)}")
            raise DistributedTransactionException(str(e), 'START')
    
    def prepare_phase(self):
        """Prepare phase of two-phase commit"""
        if not self.transactions_started:
            raise DistributedTransactionException("No active transaction", 'PREPARE')
        
        try:
            self.phase = 'PREPARING'
            logger.debug("Starting prepare phase")
            
            # Flush changes to both databases but don't commit
            self.source_session.flush()
            self.dest_session.flush()
            
            self.phase = 'PREPARED'
            logger.debug("Prepare phase completed successfully")
            return True
            
        except Exception as e:
            self.phase = 'PREPARE_FAILED'
            logger.error(f"Prepare phase failed: {str(e)}")
            raise DistributedTransactionException(str(e), 'PREPARE')
    
    def commit_phase(self):
        """Commit phase of two-phase commit"""
        if self.phase != 'PREPARED':
            raise DistributedTransactionException("Transaction not in prepared state", 'COMMIT')
        
        try:
            self.phase = 'COMMITTING'
            logger.debug("Starting commit phase")
            
            # Commit both transactions
            self.source_session.commit()
            self.dest_session.commit()
            
            self.phase = 'COMMITTED'
            logger.info("Distributed transaction committed successfully")
            
        except Exception as e:
            self.phase = 'COMMIT_FAILED'
            logger.error(f"Commit phase failed: {str(e)}")
            # Attempt rollback
            self.rollback_distributed_transaction()
            raise DistributedTransactionException(str(e), 'COMMIT')
        finally:
            self.cleanup_sessions()
    
    def commit_distributed_transaction(self):
        """Execute full two-phase commit"""
        try:
            # Phase 1: Prepare
            self.prepare_phase()
            
            # Phase 2: Commit
            self.commit_phase()
            
        except Exception as e:
            logger.error(f"Distributed transaction commit failed: {str(e)}")
            raise
    
    def rollback_distributed_transaction(self):
        """Enhanced rollback with better error handling"""
        try:
            self.phase = 'ROLLING_BACK'
            super().rollback_distributed_transaction()
            self.phase = 'ROLLED_BACK'
            logger.info("Distributed transaction rolled back successfully")
            
        except Exception as e:
            self.phase = 'ROLLBACK_FAILED'
            logger.error(f"Rollback failed: {str(e)}")
            raise DistributedTransactionException(str(e), 'ROLLBACK')
    
    def get_transaction_status(self):
        """Get current transaction status"""
        return {
            'phase': self.phase,
            'transactions_started': self.transactions_started,
            'source_session_active': self.source_session is not None,
            'dest_session_active': self.dest_session is not None
        }
    
    def is_transaction_active(self):
        """Check if transaction is active"""
        return self.transactions_started and self.phase not in ['COMMITTED', 'ROLLED_BACK', 'FAILED']
    
    def force_cleanup(self):
        """Force cleanup of all resources"""
        try:
            logger.warning("Forcing transaction cleanup")
            self.phase = 'FORCE_CLEANUP'
            self.cleanup_sessions()
            logger.info("Force cleanup completed")
            
        except Exception as e:
            logger.error(f"Force cleanup failed: {str(e)}")