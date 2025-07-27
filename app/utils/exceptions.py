"""
Custom exceptions for the banking application
"""


class BankingException(Exception):
    """Base exception for banking operations"""
    
    def __init__(self, message, error_code=None, details=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def to_dict(self):
        """Convert exception to dictionary for API responses"""
        return {
            'error': {
                'code': self.error_code or 'BANKING_ERROR',
                'message': self.message,
                'details': self.details
            }
        }


class ValidationException(BankingException):
    """Exception for validation errors"""
    
    def __init__(self, message, field=None, details=None):
        super().__init__(message, 'VALIDATION_ERROR', details)
        self.field = field


class AccountException(BankingException):
    """Exception for account-related errors"""
    pass


class AccountNotFoundException(AccountException):
    """Exception when account is not found"""
    
    def __init__(self, account_no):
        super().__init__(
            f"Account {account_no} not found",
            'ACCOUNT_NOT_FOUND',
            {'account_no': account_no}
        )


class AccountInactiveException(AccountException):
    """Exception when account is inactive"""
    
    def __init__(self, account_no, status):
        super().__init__(
            f"Account {account_no} is inactive (status: {status})",
            'ACCOUNT_INACTIVE',
            {'account_no': account_no, 'status': status}
        )


class InsufficientBalanceException(AccountException):
    """Exception when account has insufficient balance"""
    
    def __init__(self, account_no, available_balance, requested_amount):
        super().__init__(
            f"Insufficient balance in account {account_no}",
            'INSUFFICIENT_BALANCE',
            {
                'account_no': account_no,
                'available_balance': float(available_balance),
                'requested_amount': float(requested_amount)
            }
        )


class AccountRestrictedException(AccountException):
    """Exception when account is restricted"""
    
    def __init__(self, account_no, restriction_type):
        super().__init__(
            f"Account {account_no} is restricted ({restriction_type})",
            'ACCOUNT_RESTRICTED',
            {'account_no': account_no, 'restriction_type': restriction_type}
        )


class TransferException(BankingException):
    """Exception for transfer-related errors"""
    pass


class TransferLimitExceededException(TransferException):
    """Exception when transfer limit is exceeded"""
    
    def __init__(self, limit_type, limit_amount, requested_amount):
        super().__init__(
            f"{limit_type} limit exceeded",
            'TRANSFER_LIMIT_EXCEEDED',
            {
                'limit_type': limit_type,
                'limit_amount': float(limit_amount),
                'requested_amount': float(requested_amount)
            }
        )


class SameAccountTransferException(TransferException):
    """Exception when trying to transfer to the same account"""
    
    def __init__(self, account_no):
        super().__init__(
            "Cannot transfer to the same account",
            'SAME_ACCOUNT_TRANSFER',
            {'account_no': account_no}
        )


class TransferNotFoundException(TransferException):
    """Exception when transfer is not found"""
    
    def __init__(self, transfer_id):
        super().__init__(
            f"Transfer {transfer_id} not found",
            'TRANSFER_NOT_FOUND',
            {'transfer_id': transfer_id}
        )


class DatabaseException(BankingException):
    """Exception for database-related errors"""
    
    def __init__(self, message, operation=None):
        super().__init__(
            message,
            'DATABASE_ERROR',
            {'operation': operation}
        )


class DistributedTransactionException(DatabaseException):
    """Exception for distributed transaction errors"""
    
    def __init__(self, message, phase=None):
        super().__init__(
            f"Distributed transaction error: {message}",
            'DISTRIBUTED_TRANSACTION_ERROR'
        )
        self.details['phase'] = phase


class BusinessRuleException(BankingException):
    """Exception for business rule violations"""
    
    def __init__(self, rule, message):
        super().__init__(
            message,
            'BUSINESS_RULE_VIOLATION',
            {'rule': rule}
        )


class CurrencyMismatchException(BusinessRuleException):
    """Exception when currencies don't match"""
    
    def __init__(self, from_currency, to_currency):
        super().__init__(
            'CURRENCY_MISMATCH',
            f"Currency mismatch: {from_currency} -> {to_currency}"
        )
        self.details.update({
            'from_currency': from_currency,
            'to_currency': to_currency
        })


class SystemException(BankingException):
    """Exception for system-level errors"""
    
    def __init__(self, message, component=None):
        super().__init__(
            message,
            'SYSTEM_ERROR',
            {'component': component}
        )


class TimeoutException(SystemException):
    """Exception for timeout errors"""
    
    def __init__(self, operation, timeout_seconds):
        super().__init__(
            f"Operation {operation} timed out after {timeout_seconds} seconds",
            'TIMEOUT'
        )
        self.details.update({
            'operation': operation,
            'timeout_seconds': timeout_seconds
        })