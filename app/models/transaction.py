"""
Transaction-related data models
"""

from sqlalchemy import Column, BigInteger, String, DECIMAL, DateTime, TIMESTAMP, Text, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import decimal
import uuid

Base = declarative_base()


class TransactionHistory(Base):
    """Transaction history model representing rb_tran_hist table"""
    
    __tablename__ = 'rb_tran_hist'
    
    SEQ_NO = Column(String(50), primary_key=True)
    INTERNAL_KEY = Column(BigInteger, index=True)
    CLIENT_NO = Column(String(20), index=True)
    BASE_ACCT_NO = Column(String(50), index=True)
    TRAN_TYPE = Column(String(10))
    TRAN_AMT = Column(DECIMAL(20, 2))
    PREVIOUS_BAL_AMT = Column(DECIMAL(20, 2))
    ACTUAL_BAL = Column(DECIMAL(20, 2))
    CR_DR_IND = Column(String(1))  # C for Credit, D for Debit
    TRAN_DATE = Column(DateTime, default=datetime.utcnow, index=True)
    REFERENCE = Column(String(50), index=True)
    NARRATIVE = Column(String(500))
    TRAN_STATUS = Column(String(1), default='N')  # N for Normal, F for Failed
    TRAN_TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<TransactionHistory(SEQ_NO='{self.SEQ_NO}', TRAN_TYPE='{self.TRAN_TYPE}', TRAN_AMT={self.TRAN_AMT})>"
    
    @classmethod
    def generate_seq_no(cls):
        """Generate unique sequence number"""
        return f"TXN{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:8].upper()}"
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'seq_no': self.SEQ_NO,
            'internal_key': self.INTERNAL_KEY,
            'client_no': self.CLIENT_NO,
            'account_no': self.BASE_ACCT_NO,
            'transaction_type': self.TRAN_TYPE,
            'amount': float(self.TRAN_AMT) if self.TRAN_AMT else 0.0,
            'previous_balance': float(self.PREVIOUS_BAL_AMT) if self.PREVIOUS_BAL_AMT else 0.0,
            'new_balance': float(self.ACTUAL_BAL) if self.ACTUAL_BAL else 0.0,
            'credit_debit_indicator': self.CR_DR_IND,
            'transaction_date': self.TRAN_DATE.isoformat() if self.TRAN_DATE else None,
            'reference': self.REFERENCE,
            'description': self.NARRATIVE,
            'status': self.TRAN_STATUS,
            'timestamp': self.TRAN_TIMESTAMP.isoformat() if self.TRAN_TIMESTAMP else None
        }
    
    @classmethod
    def create_debit_transaction(cls, internal_key, client_no, account_no, amount, 
                               previous_balance, new_balance, reference, description="Transfer Out"):
        """Create a debit transaction record"""
        return cls(
            SEQ_NO=cls.generate_seq_no(),
            INTERNAL_KEY=internal_key,
            CLIENT_NO=client_no,
            BASE_ACCT_NO=account_no,
            TRAN_TYPE='TRANSFER',
            TRAN_AMT=decimal.Decimal(str(amount)),
            PREVIOUS_BAL_AMT=decimal.Decimal(str(previous_balance)),
            ACTUAL_BAL=decimal.Decimal(str(new_balance)),
            CR_DR_IND='D',
            REFERENCE=reference,
            NARRATIVE=description
        )
    
    @classmethod
    def create_credit_transaction(cls, internal_key, client_no, account_no, amount,
                                previous_balance, new_balance, reference, description="Transfer In"):
        """Create a credit transaction record"""
        return cls(
            SEQ_NO=cls.generate_seq_no(),
            INTERNAL_KEY=internal_key,
            CLIENT_NO=client_no,
            BASE_ACCT_NO=account_no,
            TRAN_TYPE='TRANSFER',
            TRAN_AMT=decimal.Decimal(str(amount)),
            PREVIOUS_BAL_AMT=decimal.Decimal(str(previous_balance)),
            ACTUAL_BAL=decimal.Decimal(str(new_balance)),
            CR_DR_IND='C',
            REFERENCE=reference,
            NARRATIVE=description
        )


class TransferLog(Base):
    """Transfer log model for tracking transfer operations"""
    
    __tablename__ = 'transfer_log'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    transfer_id = Column(String(50), unique=True, nullable=False, index=True)
    from_account = Column(String(50), nullable=False, index=True)
    to_account = Column(String(50), nullable=False, index=True)
    amount = Column(DECIMAL(20, 2), nullable=False)
    currency = Column(String(3), default='CNY')
    status = Column(Enum('PENDING', 'SUCCESS', 'FAILED', 'ROLLBACK'), default='PENDING', index=True)
    error_message = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, index=True)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<TransferLog(transfer_id='{self.transfer_id}', status='{self.status}', amount={self.amount})>"
    
    @classmethod
    def generate_transfer_id(cls):
        """Generate unique transfer ID"""
        return f"TRF{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:8].upper()}"
    
    def to_dict(self):
        """Convert transfer log to dictionary"""
        return {
            'id': self.id,
            'transfer_id': self.transfer_id,
            'from_account': self.from_account,
            'to_account': self.to_account,
            'amount': float(self.amount),
            'currency': self.currency,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_status(self, status, error_message=None):
        """Update transfer status"""
        self.status = status
        if error_message:
            self.error_message = error_message
        self.updated_at = datetime.utcnow()
    
    def is_pending(self):
        """Check if transfer is pending"""
        return self.status == 'PENDING'
    
    def is_successful(self):
        """Check if transfer is successful"""
        return self.status == 'SUCCESS'
    
    def is_failed(self):
        """Check if transfer failed"""
        return self.status in ['FAILED', 'ROLLBACK']


# Create composite indexes for better query performance
Index('idx_tran_hist_account_date', TransactionHistory.BASE_ACCT_NO, TransactionHistory.TRAN_DATE)
Index('idx_tran_hist_client_date', TransactionHistory.CLIENT_NO, TransactionHistory.TRAN_DATE)
Index('idx_transfer_log_accounts', TransferLog.from_account, TransferLog.to_account)
Index('idx_transfer_log_status_date', TransferLog.status, TransferLog.created_at)