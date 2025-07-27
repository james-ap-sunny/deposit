#!/bin/bash

echo "Stopping all containers..."
docker-compose down

echo "Rebuilding banking-app container..."
docker-compose build banking-app

echo "Starting all containers..."
docker-compose up -d

echo "Checking container status..."
docker-compose ps

echo "Waiting for services to start..."
sleep 10

echo "Checking banking-app logs..."
docker-compose logs banking-app

echo "Testing API endpoints..."
echo "Health check:"
curl -v http://localhost:5000/health
echo ""

echo "Account API:"
curl -v http://localhost:5000/api/v1/accounts/6230399991006371427
echo ""

echo "Services restart complete."