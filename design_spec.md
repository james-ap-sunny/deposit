# Core Banking Transfer Transaction System - Design Specification

## 1. System Architecture

### 1.1 High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │    │   Load Balancer │    │   API Gateway   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌───────────────────────────────────────────────┐
         │              Flask Application                │
         │  ┌─────────────┐  ┌─────────────┐  ┌────────┐ │
         │  │ Transaction │  │  Account    │  │  Audit │ │
         │  │  Service    │  │  Service    │  │Service │ │
         │  └─────────────┘  └─────────────┘  └────────┘ │
         └───────────────────────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MySQL DB 1    │    │   MySQL DB 2    │    │   Redis Cache   │
│ (Source Accts)  │    │ (Target Accts)  │    │   (Sessions)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 Component Architecture
- **API Layer**: Flask REST API with request validation
- **Service Layer**: Business logic and transaction orchestration
- **Data Layer**: Database access and connection management
- **Cache Layer**: Redis for session and temporary data
- **Monitoring Layer**: Logging and metrics collection

## 2. Database Design

### 2.1 Database Schema

#### 2.1.1 Account Tables (rb_acct)
```sql
CREATE TABLE rb_acct (
    INTERNAL_KEY BIGINT PRIMARY KEY,
    CLIENT_NO VARCHAR(20) NOT NULL,
    BASE_ACCT_NO VARCHAR(50) NOT NULL,
    ACCT_NAME VARCHAR(200),
    ACCT_CCY VARCHAR(3) DEFAULT 'CNY',
    ACCT_STATUS CHAR(1) DEFAULT 'A',
    ACCT_BRANCH VARCHAR(20),
    ACCT_OPEN_DATE DATETIME,
    TRAN_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_base_acct_no (BASE_ACCT_NO),
    INDEX idx_client_no (CLIENT_NO)
);
```

#### 2.1.2 Account Balance Tables (rb_acct_balance)
```sql
CREATE TABLE rb_acct_balance (
    INTERNAL_KEY BIGINT PRIMARY KEY,
    CLIENT_NO VARCHAR(20) NOT NULL,
    TOTAL_AMOUNT DECIMAL(20,2) DEFAULT 0.00,
    LAST_CHANGE_DATE DATETIME,
    TRAN_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (INTERNAL_KEY) REFERENCES rb_acct(INTERNAL_KEY)
);
```

#### 2.1.3 Transaction History (rb_tran_hist)
```sql
CREATE TABLE rb_tran_hist (
    SEQ_NO VARCHAR(50) PRIMARY KEY,
    INTERNAL_KEY BIGINT,
    CLIENT_NO VARCHAR(20),
    BASE_ACCT_NO VARCHAR(50),
    TRAN_TYPE VARCHAR(10),
    TRAN_AMT DECIMAL(20,2),
    PREVIOUS_BAL_AMT DECIMAL(20,2),
    ACTUAL_BAL DECIMAL(20,2),
    CR_DR_IND CHAR(1),
    TRAN_DATE DATETIME,
    REFERENCE VARCHAR(50),
    NARRATIVE VARCHAR(500),
    TRAN_STATUS CHAR(1) DEFAULT 'N',
    TRAN_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_internal_key (INTERNAL_KEY),
    INDEX idx_reference (REFERENCE),
    INDEX idx_tran_date (TRAN_DATE)
);
```

#### 2.1.4 Transfer Log (transfer_log)
```sql
CREATE TABLE transfer_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    transfer_id VARCHAR(50) UNIQUE NOT NULL,
    from_account VARCHAR(50) NOT NULL,
    to_account VARCHAR(50) NOT NULL,
    amount DECIMAL(20,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'CNY',
    status ENUM('PENDING', 'SUCCESS', 'FAILED', 'ROLLBACK') DEFAULT 'PENDING',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_transfer_id (transfer_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);
```

### 2.2 Database Distribution Strategy
- **Database 1**: Source accounts and related tables
- **Database 2**: Destination accounts and related tables
- **Shared Tables**: Configuration, audit logs, transfer logs

## 3. API Design

### 3.1 Transfer Transaction API

#### 3.1.1 Process Transfer
```http
POST /api/v1/transfer
Content-Type: application/json

{
    "from_account": "6230399991006371427",
    "to_account": "6230399991006371428",
    "amount": 1000.00,
    "currency": "CNY",
    "description": "Transfer payment",
    "reference": "TXN20250107001"
}
```

**Response:**
```json
{
    "status": "success",
    "transfer_id": "TXN20250107001",
    "transaction_time": "2025-01-07T10:30:00Z",
    "from_account": "6230399991006371427",
    "to_account": "6230399991006371428",
    "amount": 1000.00,
    "currency": "CNY",
    "new_balance": 9000.00
}
```

#### 3.1.2 Query Transfer Status
```http
GET /api/v1/transfer/{transfer_id}
```

**Response:**
```json
{
    "transfer_id": "TXN20250107001",
    "status": "SUCCESS",
    "from_account": "6230399991006371427",
    "to_account": "6230399991006371428",
    "amount": 1000.00,
    "currency": "CNY",
    "created_at": "2025-01-07T10:30:00Z",
    "completed_at": "2025-01-07T10:30:02Z"
}
```

### 3.2 Account Management API

#### 3.2.1 Check Account Balance
```http
GET /api/v1/account/{account_no}/balance
```

**Response:**
```json
{
    "account_no": "6230399991006371427",
    "balance": 10000.00,
    "currency": "CNY",
    "status": "ACTIVE",
    "last_updated": "2025-01-07T10:30:00Z"
}
```

## 4. Service Design

### 4.1 Transaction Service

#### 4.1.1 Transfer Processing Flow
```python
class TransferService:
    def process_transfer(self, transfer_request):
        # 1. Validate request
        self.validate_transfer_request(transfer_request)
        
        # 2. Create transfer record
        transfer_id = self.create_transfer_record(transfer_request)
        
        # 3. Begin distributed transaction
        try:
            # 4. Lock source account
            source_account = self.lock_account(transfer_request.from_account)
            
            # 5. Validate source account and balance
            self.validate_source_account(source_account, transfer_request.amount)
            
            # 6. Lock destination account
            dest_account = self.lock_account(transfer_request.to_account)
            
            # 7. Validate destination account
            self.validate_destination_account(dest_account)
            
            # 8. Debit source account
            self.debit_account(source_account, transfer_request.amount, transfer_id)
            
            # 9. Credit destination account
            self.credit_account(dest_account, transfer_request.amount, transfer_id)
            
            # 10. Update transfer status
            self.update_transfer_status(transfer_id, 'SUCCESS')
            
            # 11. Commit transaction
            self.commit_transaction()
            
            return self.get_transfer_result(transfer_id)
            
        except Exception as e:
            # Rollback transaction
            self.rollback_transaction(transfer_id, str(e))
            raise TransferException(f"Transfer failed: {str(e)}")
```

### 4.2 Account Service

#### 4.2.1 Account Operations
```python
class AccountService:
    def get_account_balance(self, account_no):
        """Get current account balance"""
        
    def lock_account_for_update(self, account_no):
        """Lock account for transaction"""
        
    def update_account_balance(self, account_no, amount, operation):
        """Update account balance (debit/credit)"""
        
    def validate_account_status(self, account_no):
        """Validate account is active and not restricted"""
```

### 4.3 Distributed Transaction Manager

#### 4.3.1 Two-Phase Commit Implementation
```python
class DistributedTransactionManager:
    def __init__(self):
        self.db1_connection = None  # Source database
        self.db2_connection = None  # Destination database
        
    def begin_transaction(self):
        """Start transaction on both databases"""
        
    def prepare_phase(self):
        """Prepare phase of 2PC"""
        
    def commit_phase(self):
        """Commit phase of 2PC"""
        
    def rollback_transaction(self):
        """Rollback transaction on both databases"""
```

## 5. Security Design

### 5.1 Authentication & Authorization
- JWT-based authentication for API access
- Role-based access control (RBAC)
- API key management for external systems

### 5.2 Data Protection
- TLS encryption for all communications
- Database connection encryption
- Sensitive data masking in logs

### 5.3 Audit & Compliance
- Complete audit trail for all operations
- Transaction logging with timestamps
- Compliance with banking regulations

## 6. Error Handling Design

### 6.1 Error Categories
- **Validation Errors**: Invalid input data
- **Business Errors**: Insufficient balance, account restrictions
- **System Errors**: Database connection, timeout issues
- **Security Errors**: Authentication, authorization failures

### 6.2 Error Response Format
```json
{
    "error": {
        "code": "INSUFFICIENT_BALANCE",
        "message": "Account balance is insufficient for this transaction",
        "details": {
            "account": "6230399991006371427",
            "available_balance": 500.00,
            "requested_amount": 1000.00
        },
        "timestamp": "2025-01-07T10:30:00Z",
        "trace_id": "abc123def456"
    }
}
```

## 7. Performance Design

### 7.1 Database Optimization
- Connection pooling for database connections
- Proper indexing on frequently queried columns
- Query optimization and caching strategies

### 7.2 Caching Strategy
- Redis for session management
- Account balance caching with TTL
- Configuration data caching

### 7.3 Monitoring & Metrics
- Transaction processing time metrics
- Database connection pool monitoring
- Error rate and success rate tracking

## 8. Deployment Architecture

### 8.1 Container Design
- **Application Container**: Flask app with gunicorn
- **Database Containers**: MySQL instances
- **Cache Container**: Redis instance
- **Monitoring Container**: Prometheus/Grafana

### 8.2 Docker Compose Structure
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db1
      - db2
      - redis
      
  db1:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: bank_db1
      
  db2:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: bank_db2
      
  redis:
    image: redis:alpine
```

This design specification provides a comprehensive blueprint for implementing the core banking transfer transaction system with proper distributed transaction handling, security measures, and scalability considerations.