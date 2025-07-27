"""
Account service for account-related business operations
"""

import logging
from decimal import Decimal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from app.models.account import Account, AccountBalance
from app.models.constraints import AccountRestraint, ClientTransactionLimit
from app.utils.exceptions import (
    AccountNotFoundException, AccountInactiveException, 
    InsufficientBalanceException, AccountRestrictedException,
    TransferLimitExceededException
)

logger = logging.getLogger(__name__)


class AccountService:
    """Service for account operations"""
    
    def __init__(self, session):
        self.session = session
    
    def get_account_by_number(self, account_no):
        """Get account by account number"""
        try:
            account = self.session.query(Account).filter(
                Account.BASE_ACCT_NO == account_no
            ).first()
            
            if not account:
                raise AccountNotFoundException(account_no)
            
            return account
            
        except Exception as e:
            logger.error(f"Error getting account {account_no}: {str(e)}")
            raise
    
    def get_account_balance(self, account_no):
        """Get account balance by account number"""
        try:
            # Join account and balance tables
            result = self.session.query(Account, AccountBalance).join(
                AccountBalance, Account.INTERNAL_KEY == AccountBalance.INTERNAL_KEY
            ).filter(Account.BASE_ACCT_NO == account_no).first()
            
            if not result:
                raise AccountNotFoundException(account_no)
            
            account, balance = result
            return account, balance
            
        except Exception as e:
            logger.error(f"Error getting balance for account {account_no}: {str(e)}")
            raise
    
    def validate_account_for_transfer(self, account_no, is_source=True):
        """Validate account for transfer operations"""
        try:
            account, balance = self.get_account_balance(account_no)
            
            # Check if account is active
            if not account.is_active():
                raise AccountInactiveException(account_no, account.ACCT_STATUS)
            
            # Check for account restrictions
            restrictions = self.get_account_restrictions(account.INTERNAL_KEY)
            active_restrictions = [r for r in restrictions if r.affects_transfers()]
            
            if active_restrictions:
                restriction_types = [r.RESTRAINT_TYPE for r in active_restrictions]
                raise AccountRestrictedException(account_no, ', '.join(restriction_types))
            
            return account, balance
            
        except Exception as e:
            logger.error(f"Account validation failed for {account_no}: {str(e)}")
            raise
    
    def get_account_restrictions(self, internal_key):
        """Get active restrictions for an account"""
        try:
            restrictions = self.session.query(AccountRestraint).filter(
                and_(
                    AccountRestraint.INTERNAL_KEY == internal_key,
                    AccountRestraint.RESTRAINTS_STATUS == 'A'
                )
            ).all()
            
            return restrictions
            
        except Exception as e:
            logger.error(f"Error getting restrictions for account {internal_key}: {str(e)}")
            raise
    
    def check_transfer_limits(self, account_no, amount):
        """Check if transfer amount is within limits"""
        try:
            # Get daily transfer limit
            daily_limit = self.session.query(ClientTransactionLimit).filter(
                and_(
                    ClientTransactionLimit.BASE_ACCT_NO == account_no,
                    ClientTransactionLimit.LIMIT_REF == 'DailyTransferLimit'
                )
            ).first()
            
            if daily_limit:
                is_valid, message = daily_limit.is_amount_within_limits(amount)
                if not is_valid:
                    if amount > daily_limit.LIMIT_MAX_AMT:
                        raise TransferLimitExceededException(
                            'Daily Transfer Limit',
                            daily_limit.LIMIT_MAX_AMT,
                            amount
                        )
                    elif amount < daily_limit.LIMIT_MIN_AMT:
                        raise TransferLimitExceededException(
                            'Minimum Transfer Amount',
                            daily_limit.LIMIT_MIN_AMT,
                            amount
                        )
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking transfer limits for {account_no}: {str(e)}")
            raise
    
    def validate_sufficient_balance(self, account_no, amount):
        """Validate if account has sufficient balance"""
        try:
            account, balance = self.get_account_balance(account_no)
            
            if not balance.has_sufficient_balance(amount):
                raise InsufficientBalanceException(
                    account_no, 
                    balance.TOTAL_AMOUNT, 
                    amount
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Balance validation failed for {account_no}: {str(e)}")
            raise
    
    def lock_account_for_update(self, account_no):
        """Lock account balance for update (SELECT FOR UPDATE)"""
        try:
            # Lock both account and balance records
            result = self.session.query(Account, AccountBalance).join(
                AccountBalance, Account.INTERNAL_KEY == AccountBalance.INTERNAL_KEY
            ).filter(Account.BASE_ACCT_NO == account_no).with_for_update().first()
            
            if not result:
                raise AccountNotFoundException(account_no)
            
            account, balance = result
            logger.debug(f"Account {account_no} locked for update")
            return account, balance
            
        except Exception as e:
            logger.error(f"Error locking account {account_no}: {str(e)}")
            raise
    
    def debit_account(self, account_no, amount, reference, description="Transfer Out"):
        """Debit amount from account"""
        try:
            # Lock account for update
            account, balance = self.lock_account_for_update(account_no)
            
            # Validate sufficient balance
            if not balance.has_sufficient_balance(amount):
                raise InsufficientBalanceException(
                    account_no, 
                    balance.TOTAL_AMOUNT, 
                    amount
                )
            
            # Record previous balance
            previous_balance = balance.TOTAL_AMOUNT
            
            # Debit the amount
            new_balance = balance.debit(amount)
            
            logger.info(f"Debited {amount} from account {account_no}. "
                       f"Previous: {previous_balance}, New: {new_balance}")
            
            return {
                'account': account,
                'previous_balance': previous_balance,
                'new_balance': new_balance,
                'amount': amount
            }
            
        except Exception as e:
            logger.error(f"Error debiting account {account_no}: {str(e)}")
            raise
    
    def credit_account(self, account_no, amount, reference, description="Transfer In"):
        """Credit amount to account"""
        try:
            # Lock account for update
            account, balance = self.lock_account_for_update(account_no)
            
            # Record previous balance
            previous_balance = balance.TOTAL_AMOUNT
            
            # Credit the amount
            new_balance = balance.credit(amount)
            
            logger.info(f"Credited {amount} to account {account_no}. "
                       f"Previous: {previous_balance}, New: {new_balance}")
            
            return {
                'account': account,
                'previous_balance': previous_balance,
                'new_balance': new_balance,
                'amount': amount
            }
            
        except Exception as e:
            logger.error(f"Error crediting account {account_no}: {str(e)}")
            raise
    
    def get_account_transaction_history(self, account_no, limit=10, offset=0):
        """Get transaction history for an account"""
        try:
            from app.models.transaction import TransactionHistory
            
            transactions = self.session.query(TransactionHistory).filter(
                TransactionHistory.BASE_ACCT_NO == account_no
            ).order_by(
                TransactionHistory.TRAN_DATE.desc()
            ).limit(limit).offset(offset).all()
            
            return [tx.to_dict() for tx in transactions]
            
        except Exception as e:
            logger.error(f"Error getting transaction history for {account_no}: {str(e)}")
            raise
    
    def get_account_info(self, account_no):
        """Get complete account information"""
        try:
            account, balance = self.get_account_balance(account_no)
            
            # Get restrictions
            restrictions = self.get_account_restrictions(account.INTERNAL_KEY)
            
            # Get transaction limits
            limits = self.session.query(ClientTransactionLimit).filter(
                ClientTransactionLimit.BASE_ACCT_NO == account_no
            ).all()
            
            return {
                'account': account.to_dict(),
                'balance': balance.to_dict(),
                'restrictions': [r.to_dict() for r in restrictions],
                'limits': [l.to_dict() for l in limits]
            }
            
        except Exception as e:
            logger.error(f"Error getting account info for {account_no}: {str(e)}")
            raise