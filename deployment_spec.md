# Core Banking Transfer Transaction System - Deployment Specification

## 1. Deployment Overview

### 1.1 Deployment Strategy
- **Containerized Deployment**: Using Docker and docker-compose
- **One-Click Deployment**: Single command deployment for Ubuntu environment
- **Multi-Database Setup**: Two separate MySQL instances for distributed transactions
- **High Availability**: Load balancing and failover capabilities

### 1.2 Target Environment
- **Operating System**: Ubuntu 20.04+ LTS
- **Container Runtime**: Docker 20.10+
- **Orchestration**: Docker Compose 2.0+
- **Network**: Internal container networking with external API exposure

## 2. Infrastructure Requirements

### 2.1 Hardware Requirements

#### 2.1.1 Minimum Requirements
- **CPU**: 4 cores (2.0 GHz)
- **Memory**: 8 GB RAM
- **Storage**: 50 GB SSD
- **Network**: 1 Gbps Ethernet

#### 2.1.2 Recommended Requirements
- **CPU**: 8 cores (2.4 GHz)
- **Memory**: 16 GB RAM
- **Storage**: 100 GB SSD (with backup storage)
- **Network**: 10 Gbps Ethernet

### 2.2 Software Prerequisites
```bash
# Ubuntu 20.04+ LTS
# Docker Engine 20.10+
# Docker Compose 2.0+
# Git (for source code management)
```

## 3. Container Architecture

### 3.1 Service Containers

#### 3.1.1 Application Container (banking-app)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### 3.1.2 Database Containers
- **bank-db1**: Source accounts database (MySQL 8.0)
- **bank-db2**: Destination accounts database (MySQL 8.0)
- **Configuration**: Optimized for banking workloads

#### 3.1.3 Cache Container
- **Redis**: Session management and caching
- **Configuration**: Persistence enabled for critical data

#### 3.1.4 Monitoring Containers
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards
- **ELK Stack**: Log aggregation and analysis

### 3.2 Network Architecture
```yaml
networks:
  banking-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 4. Docker Compose Configuration

### 4.1 Main docker-compose.yml
```yaml
version: '3.8'

services:
  # Application Service
  banking-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: banking-app
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DB1_HOST=bank-db1
      - DB1_PORT=3306
      - DB1_NAME=bank_source
      - DB1_USER=bank_user
      - DB1_PASSWORD=secure_password
      - DB2_HOST=bank-db2
      - DB2_PORT=3306
      - DB2_NAME=bank_dest
      - DB2_USER=bank_user
      - DB2_PASSWORD=secure_password
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - bank-db1
      - bank-db2
      - redis
    networks:
      - banking-network
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Source Database
  bank-db1:
    image: mysql:8.0
    container_name: bank-db1
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: bank_source
      MYSQL_USER: bank_user
      MYSQL_PASSWORD: secure_password
    ports:
      - "3306:3306"
    volumes:
      - db1_data:/var/lib/mysql
      - ./sql/init_db1.sql:/docker-entrypoint-initdb.d/init.sql
      - ./config/mysql/my.cnf:/etc/mysql/conf.d/my.cnf
    networks:
      - banking-network
    restart: unless-stopped
    command: --default-authentication-plugin=mysql_native_password

  # Destination Database
  bank-db2:
    image: mysql:8.0
    container_name: bank-db2
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: bank_dest
      MYSQL_USER: bank_user
      MYSQL_PASSWORD: secure_password
    ports:
      - "3307:3306"
    volumes:
      - db2_data:/var/lib/mysql
      - ./sql/init_db2.sql:/docker-entrypoint-initdb.d/init.sql
      - ./config/mysql/my.cnf:/etc/mysql/conf.d/my.cnf
    networks:
      - banking-network
    restart: unless-stopped
    command: --default-authentication-plugin=mysql_native_password

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: banking-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./config/redis/redis.conf:/usr/local/etc/redis/redis.conf
    networks:
      - banking-network
    restart: unless-stopped
    command: redis-server /usr/local/etc/redis/redis.conf

  # Load Balancer (Nginx)
  nginx:
    image: nginx:alpine
    container_name: banking-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./config/nginx/ssl:/etc/nginx/ssl
    depends_on:
      - banking-app
    networks:
      - banking-network
    restart: unless-stopped

  # Monitoring - Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: banking-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - banking-network
    restart: unless-stopped

  # Monitoring - Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: banking-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./config/grafana/datasources:/etc/grafana/provisioning/datasources
    networks:
      - banking-network
    restart: unless-stopped

volumes:
  db1_data:
  db2_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  banking-network:
    driver: bridge
```

## 5. Configuration Management

### 5.1 Environment Configuration
```bash
# .env file
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Database Configuration
DB1_HOST=bank-db1
DB1_PORT=3306
DB1_NAME=bank_source
DB1_USER=bank_user
DB1_PASSWORD=secure_password

DB2_HOST=bank-db2
DB2_PORT=3306
DB2_NAME=bank_dest
DB2_USER=bank_user
DB2_PASSWORD=secure_password

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# Application Configuration
MAX_TRANSFER_AMOUNT=50000.00
DAILY_TRANSFER_LIMIT=100000.00
TRANSACTION_TIMEOUT=30
```

### 5.2 Database Configuration
```ini
# config/mysql/my.cnf
[mysqld]
# Performance Settings
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 1
sync_binlog = 1

# Connection Settings
max_connections = 200
max_connect_errors = 100000

# Binary Logging (for replication)
log-bin = mysql-bin
binlog_format = ROW
expire_logs_days = 7

# Character Set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Time Zone
default-time-zone = '+08:00'

# Security
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO
```

### 5.3 Nginx Configuration
```nginx
# config/nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream banking_app {
        server banking-app:5000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://banking_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://banking_app/health;
        }
    }
}
```

## 6. Deployment Scripts

### 6.1 One-Click Deployment Script
```bash
#!/bin/bash
# deploy.sh - One-click deployment script

set -e

echo "=== Core Banking System Deployment ==="

# Check prerequisites
check_prerequisites() {
    echo "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo "Docker is not installed. Installing..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "Docker Compose is not installed. Installing..."
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    echo "Prerequisites check completed."
}

# Setup environment
setup_environment() {
    echo "Setting up environment..."
    
    # Create necessary directories
    mkdir -p logs config/{mysql,nginx,redis,prometheus,grafana} sql
    
    # Set permissions
    chmod 755 logs
    
    echo "Environment setup completed."
}

# Deploy services
deploy_services() {
    echo "Deploying services..."
    
    # Pull latest images
    docker-compose pull
    
    # Build application image
    docker-compose build
    
    # Start services
    docker-compose up -d
    
    echo "Services deployed successfully."
}

# Health check
health_check() {
    echo "Performing health check..."
    
    # Wait for services to start
    sleep 30
    
    # Check application health
    if curl -f http://localhost:5000/health; then
        echo "Application is healthy."
    else
        echo "Application health check failed."
        exit 1
    fi
    
    # Check database connections
    docker-compose exec banking-app python -c "
from app.database import test_connections
if test_connections():
    print('Database connections successful.')
else:
    print('Database connection failed.')
    exit(1)
"
}

# Main deployment flow
main() {
    check_prerequisites
    setup_environment
    deploy_services
    health_check
    
    echo "=== Deployment Completed Successfully ==="
    echo "Application URL: http://localhost:5000"
    echo "Grafana Dashboard: http://localhost:3000 (admin/admin123)"
    echo "Prometheus: http://localhost:9090"
    echo ""
    echo "To stop services: docker-compose down"
    echo "To view logs: docker-compose logs -f"
}

# Execute main function
main "$@"
```

### 6.2 Database Initialization Script
```bash
#!/bin/bash
# init_db.sh - Database initialization script

echo "Initializing databases..."

# Wait for databases to be ready
echo "Waiting for databases to start..."
sleep 20

# Initialize source database
docker-compose exec bank-db1 mysql -u root -proot_password -e "
CREATE DATABASE IF NOT EXISTS bank_source;
USE bank_source;
SOURCE /docker-entrypoint-initdb.d/init.sql;
"

# Initialize destination database
docker-compose exec bank-db2 mysql -u root -proot_password -e "
CREATE DATABASE IF NOT EXISTS bank_dest;
USE bank_dest;
SOURCE /docker-entrypoint-initdb.d/init.sql;
"

echo "Database initialization completed."
```

### 6.3 Backup Script
```bash
#!/bin/bash
# backup.sh - Database backup script

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

echo "Creating database backups..."

# Backup source database
docker-compose exec bank-db1 mysqldump -u root -proot_password bank_source > $BACKUP_DIR/bank_source.sql

# Backup destination database
docker-compose exec bank-db2 mysqldump -u root -proot_password bank_dest > $BACKUP_DIR/bank_dest.sql

echo "Backup completed: $BACKUP_DIR"
```

## 7. Security Configuration

### 7.1 SSL/TLS Configuration
```bash
# Generate SSL certificates
mkdir -p config/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout config/nginx/ssl/banking.key \
    -out config/nginx/ssl/banking.crt \
    -subj "/C=CN/ST=ZJ/L=TZ/O=Bank/CN=localhost"
```

### 7.2 Firewall Configuration
```bash
# UFW firewall rules
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3000/tcp  # Grafana (optional, for monitoring)
sudo ufw --force enable
```

## 8. Monitoring and Logging

### 8.1 Prometheus Configuration
```yaml
# config/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'banking-app'
    static_configs:
      - targets: ['banking-app:5000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'mysql-db1'
    static_configs:
      - targets: ['bank-db1:9104']

  - job_name: 'mysql-db2'
    static_configs:
      - targets: ['bank-db2:9104']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

### 8.2 Log Configuration
```python
# Logging configuration in application
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/banking.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
```

## 9. Maintenance and Operations

### 9.1 Update Procedure
```bash
#!/bin/bash
# update.sh - Application update script

echo "Updating banking application..."

# Pull latest code
git pull origin main

# Rebuild application
docker-compose build banking-app

# Rolling update
docker-compose up -d --no-deps banking-app

echo "Update completed."
```

### 9.2 Scaling Configuration
```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  banking-app:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## 10. Troubleshooting Guide

### 10.1 Common Issues

#### 10.1.1 Database Connection Issues
```bash
# Check database status
docker-compose ps
docker-compose logs bank-db1
docker-compose logs bank-db2

# Test database connectivity
docker-compose exec banking-app python -c "
from app.database import test_connections
test_connections()
"
```

#### 10.1.2 Application Performance Issues
```bash
# Check resource usage
docker stats

# Check application logs
docker-compose logs -f banking-app

# Monitor database performance
docker-compose exec bank-db1 mysql -u root -proot_password -e "SHOW PROCESSLIST;"
```

### 10.2 Recovery Procedures

#### 10.2.1 Database Recovery
```bash
# Stop services
docker-compose down

# Restore from backup
docker-compose up -d bank-db1 bank-db2
sleep 30

# Restore database
docker-compose exec bank-db1 mysql -u root -proot_password bank_source < backups/latest/bank_source.sql
docker-compose exec bank-db2 mysql -u root -proot_password bank_dest < backups/latest/bank_dest.sql

# Restart all services
docker-compose up -d
```

## 11. Performance Tuning

### 11.1 Database Optimization
```sql
-- MySQL performance tuning
SET GLOBAL innodb_buffer_pool_size = 2147483648;  -- 2GB
SET GLOBAL innodb_log_buffer_size = 67108864;     -- 64MB
SET GLOBAL max_connections = 500;
SET GLOBAL query_cache_size = 268435456;          -- 256MB
```

### 11.2 Application Optimization
```python
# Gunicorn configuration
bind = "0.0.0.0:5000"
workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

## 12. Compliance and Audit

### 12.1 Audit Configuration
```yaml
# Audit logging configuration
audit:
  enabled: true
  log_level: INFO
  log_file: /app/logs/audit.log
  include_request_body: true
  include_response_body: false
  sensitive_fields:
    - password
    - account_number
    - balance
```

### 12.2 Compliance Checklist
- [ ] Data encryption in transit and at rest
- [ ] Access control and authentication
- [ ] Audit trail for all transactions
- [ ] Data backup and recovery procedures
- [ ] Security monitoring and alerting
- [ ] Compliance with banking regulations

This deployment specification provides a comprehensive guide for deploying the core banking transfer transaction system in a production-ready environment with proper monitoring, security, and maintenance procedures.
