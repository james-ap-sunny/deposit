"""
Unit tests for transfer service
"""

import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from app.services.transfer_service import TransferService
from app.config.settings import Config
from app.utils.exceptions import (
    TransferException, SameAccountTransferException,
    TransferLimitExceededException
)


class TestTransferService:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.config = Config()
        self.transfer_service = TransferService(self.config)
    
    def test_validate_transfer_request_valid(self):
        """Test valid transfer request validation"""
        request = {
            'from_account': '6230399991006371427',
            'to_account': '6230399991006371430',
            'amount': 100.00,
            'currency': 'CNY'
        }
        
        # Should not raise any exception
        self.transfer_service._validate_transfer_request(request)
    
    def test_validate_transfer_request_missing_fields(self):
        """Test transfer request validation with missing fields"""
        request = {
            'from_account': '6230399991006371427',
            # Missing to_account, amount, currency
        }
        
        with pytest.raises(TransferException) as exc_info:
            self.transfer_service._validate_transfer_request(request)
        
        assert "Missing required field" in str(exc_info.value)
    
    def test_validate_transfer_request_same_account(self):
        """Test transfer request validation with same account"""
        request = {
            'from_account': '6230399991006371427',
            'to_account': '6230399991006371427',
            'amount': 100.00,
            'currency': 'CNY'
        }
        
        with pytest.raises(SameAccountTransferException):
            self.transfer_service._validate_transfer_request(request)
    
    def test_validate_transfer_request_negative_amount(self):
        """Test transfer request validation with negative amount"""
        request = {
            'from_account': '6230399991006371427',
            'to_account': '6230399991006371430',
            'amount': -100.00,
            'currency': 'CNY'
        }
        
        with pytest.raises(TransferException) as exc_info:
            self.transfer_service._validate_transfer_request(request)
        
        assert "must be positive" in str(exc_info.value)
    
    def test_validate_transfer_request_amount_too_large(self):
        """Test transfer request validation with amount exceeding limit"""
        request = {
            'from_account': '6230399991006371427',
            'to_account': '6230399991006371430',
            'amount': 100000.00,  # Exceeds max limit
            'currency': 'CNY'
        }
        
        with pytest.raises(TransferLimitExceededException):
            self.transfer_service._validate_transfer_request(request)
    
    def test_validate_transfer_request_amount_too_small(self):
        """Test transfer request validation with amount below minimum"""
        request = {
            'from_account': '6230399991006371427',
            'to_account': '6230399991006371430',
            'amount': 0.001,  # Below minimum
            'currency': 'CNY'
        }
        
        with pytest.raises(TransferLimitExceededException):
            self.transfer_service._validate_transfer_request(request)