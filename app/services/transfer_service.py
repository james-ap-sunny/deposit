"""
Transfer service for handling money transfers between accounts
"""

import logging
from decimal import Decimal
from datetime import datetime

from app.models.transaction import TransactionHistory, TransferLog
from app.services.account_service import AccountService
from app.services.transaction_manager import DistributedTransactionManager
from app.utils.exceptions import (
    TransferException, SameAccountTransferException, 
    CurrencyMismatchException, TransferLimitExceededException,
    BusinessRuleException
)
from app.utils.logger import TransactionLogger, log_transaction

logger = logging.getLogger(__name__)


class TransferService:
    """Service for transfer operations"""
    
    def __init__(self, config):
        self.config = config
        self.max_transfer_amount = Decimal(str(config.MAX_TRANSFER_AMOUNT))
        self.min_transfer_amount = Decimal(str(config.MIN_TRANSFER_AMOUNT))
        self.daily_transfer_limit = Decimal(str(config.DAILY_TRANSFER_LIMIT))
    
    def process_transfer(self, transfer_request):
        """Process a transfer between accounts in different databases"""
        
        # Generate transfer ID
        transfer_id = TransferLog.generate_transfer_id()
        
        with TransactionLogger(transfer_id, "Transfer Processing"):
            try:
                # Validate transfer request
                self._validate_transfer_request(transfer_request)
                
                # Initialize distributed transaction manager
                tx_manager = DistributedTransactionManager()
                
                # Begin distributed transaction
                tx_manager.begin_distributed_transaction()
                
                try:
                    # Create transfer log entry
                    transfer_log = self._create_transfer_log(transfer_id, transfer_request)
                    
                    # Process the transfer
                    result = self._execute_transfer(
                        tx_manager, transfer_log, transfer_request
                    )
                    
                    # Commit distributed transaction
                    tx_manager.commit_distributed_transaction()
                    
                    # Update transfer log status
                    self._update_transfer_log_in_both_dbs(
                        tx_manager, transfer_log.transfer_id, 'SUCCESS'
                    )
                    
                    log_transaction(transfer_id, "Transfer completed successfully")
                    return result
                    
                except Exception as e:
                    # Rollback distributed transaction
                    tx_manager.rollback_distributed_transaction()
                    
                    # Update transfer log status
                    self._update_transfer_log_in_both_dbs(
                        tx_manager, transfer_log.transfer_id, 'ROLLBACK', str(e)
                    )
                    
                    log_transaction(transfer_id, f"Transfer failed: {str(e)}", level='ERROR')
                    raise TransferException(f"Transfer failed: {str(e)}")
                
            except Exception as e:
                logger.error(f"Transfer processing error: {str(e)}")
                raise
    
    def _validate_transfer_request(self, request):
        """Validate transfer request"""
        
        # Check required fields
        required_fields = ['from_account', 'to_account', 'amount', 'currency']
        for field in required_fields:
            if not request.get(field):
                raise TransferException(f"Missing required field: {field}")
        
        # Check same account transfer
        if request['from_account'] == request['to_account']:
            raise SameAccountTransferException(request['from_account'])
        
        # Validate amount
        amount = Decimal(str(request['amount']))
        if amount <= 0:
            raise TransferException("Transfer amount must be positive")
        
        if amount < self.min_transfer_amount:
            raise TransferLimitExceededException(
                'Minimum Transfer Amount',
                self.min_transfer_amount,
                amount
            )
        
        if amount > self.max_transfer_amount:
            raise TransferLimitExceededException(
                'Maximum Transfer Amount',
                self.max_transfer_amount,
                amount
            )
        
        # Validate currency
        if request['currency'] != 'CNY':
            raise CurrencyMismatchException(request['currency'], 'CNY')
    
    def _create_transfer_log(self, transfer_id, request):
        """Create transfer log entry"""
        transfer_log = TransferLog(
            transfer_id=transfer_id,
            from_account=request['from_account'],
            to_account=request['to_account'],
            amount=Decimal(str(request['amount'])),
            currency=request['currency'],
            status='PENDING'
        )
        
        return transfer_log
    
    def _execute_transfer(self, tx_manager, transfer_log, request):
        """Execute the actual transfer"""
        
        from_account = request['from_account']
        to_account = request['to_account']
        amount = Decimal(str(request['amount']))
        reference = transfer_log.transfer_id
        
        # Get database sessions
        source_session = tx_manager.get_source_session()
        dest_session = tx_manager.get_dest_session()
        
        # Initialize account services
        source_account_service = AccountService(source_session)
        dest_account_service = AccountService(dest_session)
        
        # Step 1: Validate and lock source account
        log_transaction(reference, "Validating source account")
        source_account, source_balance = source_account_service.validate_account_for_transfer(
            from_account, is_source=True
        )
        
        # Check transfer limits for source account
        source_account_service.check_transfer_limits(from_account, amount)
        
        # Validate sufficient balance
        source_account_service.validate_sufficient_balance(from_account, amount)
        
        # Step 2: Validate destination account
        log_transaction(reference, "Validating destination account")
        dest_account, dest_balance = dest_account_service.validate_account_for_transfer(
            to_account, is_source=False
        )
        
        # Check currency compatibility
        if not source_account.is_same_currency(dest_account.ACCT_CCY):
            raise CurrencyMismatchException(source_account.ACCT_CCY, dest_account.ACCT_CCY)
        
        # Step 3: Add transfer log to both databases
        source_session.add(transfer_log)
        dest_session.add(TransferLog(
            transfer_id=transfer_log.transfer_id,
            from_account=transfer_log.from_account,
            to_account=transfer_log.to_account,
            amount=transfer_log.amount,
            currency=transfer_log.currency,
            status='PENDING'
        ))
        
        # Step 4: Debit source account
        log_transaction(reference, f"Debiting {amount} from {from_account}")
        debit_result = source_account_service.debit_account(
            from_account, amount, reference, 
            f"Transfer to {to_account}"
        )
        
        # Step 5: Credit destination account
        log_transaction(reference, f"Crediting {amount} to {to_account}")
        credit_result = dest_account_service.credit_account(
            to_account, amount, reference,
            f"Transfer from {from_account}"
        )
        
        # Step 6: Create transaction history records
        self._create_transaction_history(
            source_session, debit_result, reference, 'D'
        )
        
        self._create_transaction_history(
            dest_session, credit_result, reference, 'C'
        )
        
        # Prepare result
        result = {
            'transfer_id': reference,
            'from_account': from_account,
            'to_account': to_account,
            'amount': float(amount),
            'currency': request['currency'],
            'status': 'SUCCESS',
            'source_new_balance': float(debit_result['new_balance']),
            'dest_new_balance': float(credit_result['new_balance']),
            'transaction_time': datetime.utcnow().isoformat()
        }
        
        return result
    
    def _create_transaction_history(self, session, account_result, reference, cr_dr_ind):
        """Create transaction history record"""
        
        account = account_result['account']
        
        if cr_dr_ind == 'D':
            # Debit transaction
            transaction = TransactionHistory.create_debit_transaction(
                internal_key=account.INTERNAL_KEY,
                client_no=account.CLIENT_NO,
                account_no=account.BASE_ACCT_NO,
                amount=account_result['amount'],
                previous_balance=account_result['previous_balance'],
                new_balance=account_result['new_balance'],
                reference=reference,
                description="Transfer Out"
            )
        else:
            # Credit transaction
            transaction = TransactionHistory.create_credit_transaction(
                internal_key=account.INTERNAL_KEY,
                client_no=account.CLIENT_NO,
                account_no=account.BASE_ACCT_NO,
                amount=account_result['amount'],
                previous_balance=account_result['previous_balance'],
                new_balance=account_result['new_balance'],
                reference=reference,
                description="Transfer In"
            )
        
        session.add(transaction)
    
    def _update_transfer_log_in_both_dbs(self, tx_manager, transfer_id, status, error_message=None):
        """Update transfer log status in both databases"""
        try:
            # Update in source database
            source_session = tx_manager.get_source_session()
            source_log = source_session.query(TransferLog).filter(
                TransferLog.transfer_id == transfer_id
            ).first()
            if source_log:
                source_log.update_status(status, error_message)
            
            # Update in destination database
            dest_session = tx_manager.get_dest_session()
            dest_log = dest_session.query(TransferLog).filter(
                TransferLog.transfer_id == transfer_id
            ).first()
            if dest_log:
                dest_log.update_status(status, error_message)
            
        except Exception as e:
            logger.error(f"Error updating transfer log status: {str(e)}")
    
    def get_transfer_status(self, transfer_id):
        """Get transfer status by transfer ID"""
        try:
            # Try to get from source database first
            from app.database.connection import get_source_session
            
            with get_source_session() as session:
                transfer_log = session.query(TransferLog).filter(
                    TransferLog.transfer_id == transfer_id
                ).first()
                
                if transfer_log:
                    return transfer_log.to_dict()
                
                # If not found in source, try destination database
                from app.database.connection import get_dest_session
                
                with get_dest_session() as session:
                    transfer_log = session.query(TransferLog).filter(
                        TransferLog.transfer_id == transfer_id
                    ).first()
                    
                    if transfer_log:
                        return transfer_log.to_dict()
                
                return None
                
        except Exception as e:
            logger.error(f"Error getting transfer status: {str(e)}")
            raise
    
    def get_transfer_history(self, account_no, limit=10, offset=0):
        """Get transfer history for an account"""
        try:
            # This would need to query both databases and merge results
            # For now, we'll implement a basic version
            from app.database.connection import get_source_session, get_dest_session
            
            transfers = []
            
            # Get transfers from source database (outgoing)
            with get_source_session() as session:
                source_transfers = session.query(TransferLog).filter(
                    TransferLog.from_account == account_no
                ).order_by(TransferLog.created_at.desc()).limit(limit).all()
                transfers.extend([t.to_dict() for t in source_transfers])
            
            # Get transfers from destination database (incoming)
            with get_dest_session() as session:
                dest_transfers = session.query(TransferLog).filter(
                    TransferLog.to_account == account_no
                ).order_by(TransferLog.created_at.desc()).limit(limit).all()
                transfers.extend([t.to_dict() for t in dest_transfers])
            
            # Sort by created_at and apply limit
            transfers.sort(key=lambda x: x['created_at'], reverse=True)
            return transfers[offset:offset+limit]
            
        except Exception as e:
            logger.error(f"Error getting transfer history: {str(e)}")
            raise