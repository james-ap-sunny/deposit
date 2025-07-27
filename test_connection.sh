#!/bin/bash
# Script to test the database connection after applying the fix

echo "=== Testing Database Connection ==="

# Check if the banking-app container is running
echo "Checking container status..."
docker-compose ps banking-app

# Check the logs for successful database connection
echo "Checking logs for successful database connection..."
docker-compose logs --tail=50 banking-app | grep -i "database connections initialized successfully"

# Test the health endpoint
echo "Testing health endpoint..."
curl -v http://localhost:5000/health

# Test the account API
echo "Testing account API..."
curl -v http://localhost:5000/api/v1/accounts/6230399991006371427

echo "Test complete."