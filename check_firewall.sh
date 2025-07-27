#!/bin/bash

# Check if UFW is active
echo "Checking UFW status..."
sudo ufw status

# Allow port 5000 if UFW is active
echo "Allowing port 5000 through UFW..."
sudo ufw allow 5000/tcp

# Check if iptables is blocking port 5000
echo "Checking iptables rules for port 5000..."
sudo iptables -L | grep 5000

# Add iptables rule to allow port 5000 if needed
echo "Adding iptables rule to allow port 5000..."
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT

echo "Firewall configuration complete."