"""
Constraint and limit-related data models
"""

from sqlalchemy import Column, BigInteger, String, DECIMAL, DateTime, TIMESTAMP, Date, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date
import decimal

Base = declarative_base()


class AccountRestraint(Base):
    """Account restraint model representing rb_restraints table"""
    
    __tablename__ = 'rb_restraints'
    
    INTERNAL_KEY = Column(BigInteger, primary_key=True)
    RESTRAINT_TYPE = Column(String(10), primary_key=True, index=True)
    RES_SEQ_NO = Column(String(20), primary_key=True)
    CLIENT_NO = Column(String(20), index=True)
    REAL_RESTRAINT_AMT = Column(DECIMAL(20, 2), default=decimal.Decimal('0.00'))
    RESTRAINTS_STATUS = Column(String(1), default='A')  # A for Active, I for Inactive
    TRAN_TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AccountRestraint(INTERNAL_KEY={self.INTERNAL_KEY}, RESTRAINT_TYPE='{self.RESTRAINT_TYPE}')>"
    
    def to_dict(self):
        """Convert restraint to dictionary"""
        return {
            'internal_key': self.INTERNAL_KEY,
            'restraint_type': self.RESTRAINT_TYPE,
            'sequence_no': self.RES_SEQ_NO,
            'client_no': self.CLIENT_NO,
            'restraint_amount': float(self.REAL_RESTRAINT_AMT),
            'status': self.RESTRAINTS_STATUS,
            'timestamp': self.TRAN_TIMESTAMP.isoformat() if self.TRAN_TIMESTAMP else None
        }
    
    def is_active(self):
        """Check if restraint is active"""
        return self.RESTRAINTS_STATUS == 'A'
    
    def is_freeze_restraint(self):
        """Check if this is a freeze restraint"""
        return self.RESTRAINT_TYPE in ['FREEZE', 'JUDICIAL', 'ADMIN']
    
    def affects_transfers(self):
        """Check if this restraint affects transfers"""
        return self.is_active() and self.is_freeze_restraint()


class ClientTransactionLimit(Base):
    """Client transaction limit model representing rb_lm_client_tran_limit table"""
    
    __tablename__ = 'rb_lm_client_tran_limit'
    
    BASE_ACCT_NO = Column(String(50), primary_key=True)
    LIMIT_REF = Column(String(50), primary_key=True)
    ACCT_CCY = Column(String(3))
    CLIENT_NO = Column(String(20), index=True)
    LIMIT_MAX_AMT = Column(DECIMAL(20, 2))
    LIMIT_MIN_AMT = Column(DECIMAL(20, 2))
    TRAN_DATE = Column(Date, default=date.today)
    TRAN_TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ClientTransactionLimit(BASE_ACCT_NO='{self.BASE_ACCT_NO}', LIMIT_REF='{self.LIMIT_REF}')>"
    
    def to_dict(self):
        """Convert limit to dictionary"""
        return {
            'account_no': self.BASE_ACCT_NO,
            'limit_reference': self.LIMIT_REF,
            'currency': self.ACCT_CCY,
            'client_no': self.CLIENT_NO,
            'max_amount': float(self.LIMIT_MAX_AMT) if self.LIMIT_MAX_AMT else None,
            'min_amount': float(self.LIMIT_MIN_AMT) if self.LIMIT_MIN_AMT else None,
            'transaction_date': self.TRAN_DATE.isoformat() if self.TRAN_DATE else None,
            'timestamp': self.TRAN_TIMESTAMP.isoformat() if self.TRAN_TIMESTAMP else None
        }
    
    def is_amount_within_limits(self, amount):
        """Check if amount is within the defined limits"""
        amount_decimal = decimal.Decimal(str(amount))
        
        # Check minimum limit
        if self.LIMIT_MIN_AMT and amount_decimal < self.LIMIT_MIN_AMT:
            return False, f"Amount {amount} is below minimum limit {self.LIMIT_MIN_AMT}"
        
        # Check maximum limit
        if self.LIMIT_MAX_AMT and amount_decimal > self.LIMIT_MAX_AMT:
            return False, f"Amount {amount} exceeds maximum limit {self.LIMIT_MAX_AMT}"
        
        return True, "Amount is within limits"
    
    def is_daily_transfer_limit(self):
        """Check if this is a daily transfer limit"""
        return self.LIMIT_REF in ['DailyTransferLimit', 'RcNotMtTransferLimitPd']
    
    def is_current_date(self):
        """Check if the limit is for current date"""
        return self.TRAN_DATE == date.today()


# Create indexes for better performance
Index('idx_restraints_client_type', AccountRestraint.CLIENT_NO, AccountRestraint.RESTRAINT_TYPE)
Index('idx_restraints_status', AccountRestraint.RESTRAINTS_STATUS)
Index('idx_limits_client', ClientTransactionLimit.CLIENT_NO)
Index('idx_limits_ref_date', ClientTransactionLimit.LIMIT_REF, ClientTransactionLimit.TRAN_DATE)