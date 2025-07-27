# Core Banking Transfer Transaction System

A distributed core banking system for handling money transfers between accounts across multiple MySQL databases using Python Flask.

## Features

- ✅ **Distributed Transactions**: Two-phase commit across multiple MySQL databases
- ✅ **Account Management**: Account validation, balance checking, and transaction history
- ✅ **Transfer Processing**: Secure money transfers with comprehensive validation
- ✅ **Business Rules**: Configurable transfer limits and validation rules
- ✅ **Audit Trail**: Complete transaction logging and audit capabilities
- ✅ **RESTful API**: Clean REST API with comprehensive error handling
- ✅ **Docker Deployment**: One-click deployment with Docker Compose
- ✅ **Health Monitoring**: Built-in health checks and monitoring endpoints
- ✅ **Security**: JWT authentication and input validation

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Source DB     │    │ Destination DB  │
│   (MySQL)       │    │   (MySQL)       │
│                 │    │                 │
│ - Accounts      │    │ - Accounts      │
│ - Balances      │    │ - Balances      │
│ - Transactions  │    │ - Transactions  │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌─────────────────┐
         │  Flask App      │
         │                 │
         │ - Transfer API  │
         │ - Account API   │
         │ - Health API    │
         └─────────────────┘
                     │
         ┌─────────────────┐
         │   Redis Cache   │
         │                 │
         │ - Sessions      │
         │ - Temp Data     │
         └─────────────────┘
```

## Quick Start

### Prerequisites

- Ubuntu 20.04+ LTS
- Docker 20.10+
- Docker Compose 2.0+

### One-Click Deployment

```bash
# Clone the repository
git clone <repository-url>
cd banking-system

# Make deployment script executable
chmod +x deploy.sh

# Run one-click deployment
./deploy.sh
```

The deployment script will:
1. Install Docker and Docker Compose if needed
2. Set up the environment
3. Deploy all services
4. Perform health checks
5. Display service information

### Manual Deployment

```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Health Check
```bash
# Basic health check
curl http://localhost:5000/health

# Detailed health check
curl http://localhost:5000/health/detailed
```

### Account Operations

#### Get Account Information
```bash
curl http://localhost:5000/api/v1/accounts/6230399991006371427
```

#### Get Account Balance
```bash
curl http://localhost:5000/api/v1/accounts/6230399991006371427/balance
```

#### Get Transaction History
```bash
curl http://localhost:5000/api/v1/accounts/6230399991006371427/transactions?limit=10&offset=0
```

### Transfer Operations

#### Create Transfer
```bash
curl -X POST http://localhost:5000/api/v1/transfers \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "6230399991006371427",
    "to_account": "6230399991006371430", 
    "amount": 100.00,
    "currency": "CNY",
    "description": "Test transfer"
  }'
```

#### Get Transfer Status
```bash
curl http://localhost:5000/api/v1/transfers/{transfer_id}
```

#### Get Transfer History
```bash
curl http://localhost:5000/api/v1/transfers/history/6230399991006371427
```

#### Validate Transfer
```bash
curl -X POST http://localhost:5000/api/v1/transfers/validate \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "6230399991006371427",
    "to_account": "6230399991006371430",
    "amount": 100.00,
    "currency": "CNY"
  }'
```

## Configuration

### Environment Variables

Key configuration options in `.env` file:

```bash
# Business Rules
MAX_TRANSFER_AMOUNT=50000.00
DAILY_TRANSFER_LIMIT=100000.00
MIN_TRANSFER_AMOUNT=0.01

# Database Configuration
DB1_HOST=bank-db1
DB1_PORT=3306
DB1_NAME=bank_source
DB1_USER=bank_user
DB1_PASSWORD=secure_password123

DB2_HOST=bank-db2
DB2_PORT=3306
DB2_NAME=bank_dest
DB2_USER=bank_user
DB2_PASSWORD=secure_password123
```

### Sample Data

The system comes with pre-loaded sample data:

**Source Database Accounts:**
- `6230399991006371427` - 张三 (Balance: ¥10,000)
- `6230399991006371428` - 李四 (Balance: ¥15,000)
- `6230399991006371429` - 王五 (Balance: ¥8,000)

**Destination Database Accounts:**
- `6230399991006371430` - 赵六 (Balance: ¥5,000)
- `6230399991006371431` - 孙七 (Balance: ¥12,000)
- `6230399991006371432` - 周八 (Balance: ¥20,000)

## Testing

### Run Unit Tests
```bash
# Install test dependencies
pip install pytest pytest-flask pytest-mock

# Run tests
pytest tests/
```

### Manual Testing
```bash
# Test transfer between databases
curl -X POST http://localhost:5000/api/v1/transfers \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "6230399991006371427",
    "to_account": "6230399991006371430",
    "amount": 500.00
  }'

# Check balances after transfer
curl http://localhost:5000/api/v1/accounts/6230399991006371427/balance
curl http://localhost:5000/api/v1/accounts/6230399991006371430/balance
```

## Monitoring

### Service Status
```bash
# Check all services
docker-compose ps

# Check specific service logs
docker-compose logs banking-app
docker-compose logs bank-db1
docker-compose logs bank-db2
```

### Database Access
```bash
# Connect to source database
docker-compose exec bank-db1 mysql -u bank_user -p bank_source

# Connect to destination database  
docker-compose exec bank-db2 mysql -u bank_user -p bank_dest
```

## Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check Docker daemon
sudo systemctl status docker

# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

#### Database Connection Issues
```bash
# Check database status
docker-compose ps
docker-compose logs bank-db1
docker-compose logs bank-db2

# Test database connectivity
curl http://localhost:5000/health/detailed
```

#### Application Errors
```bash
# Check application logs
docker-compose logs banking-app

# Check health endpoint
curl http://localhost:5000/health
```

### Performance Tuning

#### Database Optimization
```sql
-- Check MySQL performance
SHOW PROCESSLIST;
SHOW ENGINE INNODB STATUS;

-- Optimize queries
EXPLAIN SELECT * FROM rb_acct WHERE BASE_ACCT_NO = '6230399991006371427';
```

#### Application Optimization
```bash
# Monitor resource usage
docker stats

# Scale application instances
docker-compose up -d --scale banking-app=3
```

## Security Considerations

- Change default passwords in production
- Use HTTPS in production environments
- Implement proper JWT token management
- Regular security audits and updates
- Network isolation and firewall rules
- Database access restrictions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section
- Review application logs
- Create an issue in the repository