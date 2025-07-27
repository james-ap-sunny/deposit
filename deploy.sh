#!/bin/bash
# One-click deployment script for Core Banking Transfer System

set -e

echo "=== Core Banking Transfer System Deployment ==="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if running on Ubuntu
    if ! grep -q "Ubuntu" /etc/os-release 2>/dev/null; then
        print_warning "This script is optimized for Ubuntu. Proceeding anyway..."
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_status "Docker not found. Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        print_status "Docker installed. You may need to log out and back in for group changes to take effect."
    else
        print_status "Docker is already installed."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_status "Docker Compose not found. Installing..."
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        print_status "Docker Compose installed."
    else
        print_status "Docker Compose is already installed."
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker and try again."
        exit 1
    fi
    
    print_status "Prerequisites check completed."
}

# Setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Create necessary directories
    mkdir -p logs config sql
    
    # Set permissions
    chmod 755 logs
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_status "Creating .env file..."
        cat > .env << EOF
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=change-this-secret-key-in-production
JWT_SECRET_KEY=change-this-jwt-secret-key-in-production

# Database Configuration - Source
DB1_HOST=bank-db1
DB1_PORT=3306
DB1_NAME=bank_source
DB1_USER=bank_user
DB1_PASSWORD=secure_password123

# Database Configuration - Destination
DB2_HOST=bank-db2
DB2_PORT=3306
DB2_NAME=bank_dest
DB2_USER=bank_user
DB2_PASSWORD=secure_password123

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Business Rules
MAX_TRANSFER_AMOUNT=50000.00
DAILY_TRANSFER_LIMIT=100000.00
MIN_TRANSFER_AMOUNT=0.01
TRANSACTION_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
EOF
        print_status ".env file created. Please review and update the passwords!"
    else
        print_status ".env file already exists."
    fi
    
    print_status "Environment setup completed."
}

# Deploy services
deploy_services() {
    print_status "Deploying services..."
    
    # Stop any existing containers
    print_status "Stopping existing containers..."
    docker-compose down --remove-orphans || true
    
    # Pull latest images
    print_status "Pulling Docker images..."
    docker-compose pull
    
    # Build application image
    print_status "Building application image..."
    docker-compose build banking-app
    
    # Start services
    print_status "Starting services..."
    docker-compose up -d
    
    print_status "Services deployed successfully."
}

# Health check
health_check() {
    print_status "Performing health check..."
    
    # Wait for services to start
    print_status "Waiting for services to start (30 seconds)..."
    sleep 30
    
    # Check if containers are running
    if ! docker-compose ps | grep -q "Up"; then
        print_error "Some containers are not running. Check logs with: docker-compose logs"
        return 1
    fi
    
    # Check application health
    print_status "Checking application health..."
    for i in {1..10}; do
        if curl -f http://localhost:5000/health &> /dev/null; then
            print_status "Application is healthy!"
            break
        else
            if [ $i -eq 10 ]; then
                print_error "Application health check failed after 10 attempts."
                print_error "Check logs with: docker-compose logs banking-app"
                return 1
            fi
            print_status "Waiting for application to be ready... (attempt $i/10)"
            sleep 10
        fi
    done
    
    # Check database connections
    print_status "Checking database connections..."
    if curl -f http://localhost:5000/health/detailed &> /dev/null; then
        print_status "Database connections are healthy!"
    else
        print_warning "Database health check failed. Check logs with: docker-compose logs"
    fi
    
    print_status "Health check completed."
}

# Show deployment information
show_deployment_info() {
    print_status "=== Deployment Information ==="
    echo ""
    echo "🏦 Core Banking Transfer System is now running!"
    echo ""
    echo "📊 Service URLs:"
    echo "   • Application API: http://localhost:5000"
    echo "   • Health Check: http://localhost:5000/health"
    echo "   • Detailed Health: http://localhost:5000/health/detailed"
    echo ""
    echo "🗄️  Database Ports:"
    echo "   • Source Database (MySQL): localhost:3306"
    echo "   • Destination Database (MySQL): localhost:3307"
    echo "   • Redis Cache: localhost:6379"
    echo ""
    echo "🔧 Management Commands:"
    echo "   • View logs: docker-compose logs -f"
    echo "   • Stop services: docker-compose down"
    echo "   • Restart services: docker-compose restart"
    echo "   • View status: docker-compose ps"
    echo ""
    echo "📋 Sample API Calls:"
    echo "   • Get account info: curl http://localhost:5000/api/v1/accounts/6230399991006371427"
    echo "   • Create transfer: curl -X POST http://localhost:5000/api/v1/transfers \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -d '{\"from_account\":\"6230399991006371427\",\"to_account\":\"6230399991006371430\",\"amount\":100.00}'"
    echo ""
    print_status "Deployment completed successfully! 🎉"
}

# Cleanup function
cleanup() {
    if [ -f get-docker.sh ]; then
        rm get-docker.sh
    fi
}

# Error handling
handle_error() {
    print_error "Deployment failed at step: $1"
    print_error "Check the logs above for more details."
    cleanup
    exit 1
}

# Main deployment flow
main() {
    trap cleanup EXIT
    
    echo "Starting deployment process..."
    echo ""
    
    check_prerequisites || handle_error "Prerequisites check"
    setup_environment || handle_error "Environment setup"
    deploy_services || handle_error "Service deployment"
    health_check || handle_error "Health check"
    show_deployment_info
    
    cleanup
}

# Execute main function
main "$@"