"""
Account-related data models
"""

from sqlalchemy import Column, BigInteger, String, DECIMAL, DateTime, TIMESTAMP, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import decimal

Base = declarative_base()


class Account(Base):
    """Account model representing rb_acct table"""
    
    __tablename__ = 'rb_acct'
    
    INTERNAL_KEY = Column(BigInteger, primary_key=True, autoincrement=True)
    CLIENT_NO = Column(String(20), nullable=False, index=True)
    BASE_ACCT_NO = Column(String(50), nullable=False, unique=True, index=True)
    ACCT_NAME = Column(String(200))
    ACCT_CCY = Column(String(3), default='CNY')
    ACCT_STATUS = Column(String(1), default='A', index=True)
    ACCT_BRANCH = Column(String(20))
    ACCT_OPEN_DATE = Column(DateTime, default=datetime.utcnow)
    TRAN_TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to balance
    balance = relationship("AccountBalance", back_populates="account", uselist=False)
    
    def __repr__(self):
        return f"<Account(INTERNAL_KEY={self.INTERNAL_KEY}, BASE_ACCT_NO='{self.BASE_ACCT_NO}', ACCT_NAME='{self.ACCT_NAME}')>"
    
    def to_dict(self):
        """Convert account to dictionary"""
        return {
            'internal_key': self.INTERNAL_KEY,
            'client_no': self.CLIENT_NO,
            'account_no': self.BASE_ACCT_NO,
            'account_name': self.ACCT_NAME,
            'currency': self.ACCT_CCY,
            'status': self.ACCT_STATUS,
            'branch': self.ACCT_BRANCH,
            'open_date': self.ACCT_OPEN_DATE.isoformat() if self.ACCT_OPEN_DATE else None,
            'last_updated': self.TRAN_TIMESTAMP.isoformat() if self.TRAN_TIMESTAMP else None
        }
    
    def is_active(self):
        """Check if account is active"""
        return self.ACCT_STATUS == 'A'
    
    def is_same_currency(self, currency):
        """Check if account has the same currency"""
        return self.ACCT_CCY == currency


class AccountBalance(Base):
    """Account balance model representing rb_acct_balance table"""
    
    __tablename__ = 'rb_acct_balance'
    
    INTERNAL_KEY = Column(BigInteger, ForeignKey('rb_acct.INTERNAL_KEY'), primary_key=True)
    CLIENT_NO = Column(String(20), nullable=False, index=True)
    TOTAL_AMOUNT = Column(DECIMAL(20, 2), default=decimal.Decimal('0.00'))
    LAST_CHANGE_DATE = Column(DateTime, default=datetime.utcnow)
    TRAN_TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to account
    account = relationship("Account", back_populates="balance")
    
    def __repr__(self):
        return f"<AccountBalance(INTERNAL_KEY={self.INTERNAL_KEY}, TOTAL_AMOUNT={self.TOTAL_AMOUNT})>"
    
    def to_dict(self):
        """Convert balance to dictionary"""
        return {
            'internal_key': self.INTERNAL_KEY,
            'client_no': self.CLIENT_NO,
            'balance': float(self.TOTAL_AMOUNT),
            'last_change_date': self.LAST_CHANGE_DATE.isoformat() if self.LAST_CHANGE_DATE else None,
            'last_updated': self.TRAN_TIMESTAMP.isoformat() if self.TRAN_TIMESTAMP else None
        }
    
    def has_sufficient_balance(self, amount):
        """Check if account has sufficient balance for the amount"""
        return self.TOTAL_AMOUNT >= decimal.Decimal(str(amount))
    
    def debit(self, amount):
        """Debit amount from balance"""
        amount_decimal = decimal.Decimal(str(amount))
        if not self.has_sufficient_balance(amount_decimal):
            raise ValueError(f"Insufficient balance: {self.TOTAL_AMOUNT} < {amount_decimal}")
        
        self.TOTAL_AMOUNT -= amount_decimal
        self.LAST_CHANGE_DATE = datetime.utcnow()
        return self.TOTAL_AMOUNT
    
    def credit(self, amount):
        """Credit amount to balance"""
        amount_decimal = decimal.Decimal(str(amount))
        self.TOTAL_AMOUNT += amount_decimal
        self.LAST_CHANGE_DATE = datetime.utcnow()
        return self.TOTAL_AMOUNT


# Create indexes for better performance
Index('idx_acct_client_status', Account.CLIENT_NO, Account.ACCT_STATUS)
Index('idx_balance_client', AccountBalance.CLIENT_NO)