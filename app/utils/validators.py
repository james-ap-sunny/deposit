"""
Validation utilities for the banking application
"""

import re
from decimal import Decimal, InvalidOperation
from app.utils.exceptions import ValidationException


def validate_account_number(account_no):
    """Validate account number format"""
    if not account_no:
        raise ValidationException("Account number is required", "account_no")
    
    if not isinstance(account_no, str):
        raise ValidationException("Account number must be a string", "account_no")
    
    # Check length (assuming 19 digits for Chinese bank accounts)
    if len(account_no) < 10 or len(account_no) > 50:
        raise ValidationException("Account number length must be between 10 and 50 characters", "account_no")
    
    # Check if it contains only digits and allowed characters
    if not re.match(r'^[0-9A-Za-z]+$', account_no):
        raise ValidationException("Account number contains invalid characters", "account_no")
    
    return True


def validate_amount(amount):
    """Validate transfer amount"""
    if amount is None:
        raise ValidationException("Amount is required", "amount")
    
    try:
        # Convert to Decimal for precise calculation
        decimal_amount = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        raise ValidationException("Amount must be a valid number", "amount")
    
    # Check if amount is positive
    if decimal_amount <= 0:
        raise ValidationException("Amount must be positive", "amount")
    
    # Check decimal places (max 2 for currency)
    if decimal_amount.as_tuple().exponent < -2:
        raise ValidationException("Amount cannot have more than 2 decimal places", "amount")
    
    return decimal_amount


def validate_currency(currency):
    """Validate currency code"""
    if not currency:
        raise ValidationException("Currency is required", "currency")
    
    if not isinstance(currency, str):
        raise ValidationException("Currency must be a string", "currency")
    
    # Currently only support CNY
    supported_currencies = ['CNY']
    if currency.upper() not in supported_currencies:
        raise ValidationException(f"Unsupported currency. Supported: {', '.join(supported_currencies)}", "currency")
    
    return currency.upper()


def validate_client_number(client_no):
    """Validate client number format"""
    if not client_no:
        raise ValidationException("Client number is required", "client_no")
    
    if not isinstance(client_no, str):
        raise ValidationException("Client number must be a string", "client_no")
    
    # Check length
    if len(client_no) < 5 or len(client_no) > 20:
        raise ValidationException("Client number length must be between 5 and 20 characters", "client_no")
    
    # Check format (digits only for now)
    if not re.match(r'^[0-9]+$', client_no):
        raise ValidationException("Client number must contain only digits", "client_no")
    
    return True


def validate_transfer_request(request_data):
    """Validate complete transfer request"""
    errors = []
    
    # Validate from_account
    try:
        validate_account_number(request_data.get('from_account'))
    except ValidationException as e:
        errors.append(f"from_account: {e.message}")
    
    # Validate to_account
    try:
        validate_account_number(request_data.get('to_account'))
    except ValidationException as e:
        errors.append(f"to_account: {e.message}")
    
    # Validate amount
    try:
        validate_amount(request_data.get('amount'))
    except ValidationException as e:
        errors.append(f"amount: {e.message}")
    
    # Validate currency
    try:
        validate_currency(request_data.get('currency', 'CNY'))
    except ValidationException as e:
        errors.append(f"currency: {e.message}")
    
    # Check if from_account and to_account are different
    if (request_data.get('from_account') and 
        request_data.get('to_account') and 
        request_data.get('from_account') == request_data.get('to_account')):
        errors.append("from_account and to_account cannot be the same")
    
    if errors:
        raise ValidationException(f"Validation failed: {'; '.join(errors)}")
    
    return True


def validate_pagination_params(limit, offset):
    """Validate pagination parameters"""
    try:
        limit = int(limit) if limit is not None else 10
        offset = int(offset) if offset is not None else 0
    except (ValueError, TypeError):
        raise ValidationException("Limit and offset must be integers")
    
    if limit < 1 or limit > 100:
        raise ValidationException("Limit must be between 1 and 100")
    
    if offset < 0:
        raise ValidationException("Offset must be non-negative")
    
    return limit, offset


def sanitize_string(value, max_length=None):
    """Sanitize string input"""
    if value is None:
        return None
    
    if not isinstance(value, str):
        value = str(value)
    
    # Remove leading/trailing whitespace
    value = value.strip()
    
    # Truncate if max_length specified
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    return value


def validate_date_range(start_date, end_date):
    """Validate date range"""
    from datetime import datetime, timedelta
    
    if start_date and end_date:
        if start_date > end_date:
            raise ValidationException("Start date cannot be after end date")
        
        # Check if date range is not too large (e.g., max 1 year)
        if (end_date - start_date).days > 365:
            raise ValidationException("Date range cannot exceed 365 days")
    
    return True