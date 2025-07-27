# Banking Application Troubleshooting Guide

This guide will help you diagnose and fix the issue with the banking application not being accessible via `localhost:5000`.

## 1. Check Container Status

First, check if all containers are running properly:

```bash
docker-compose ps
```

Make sure all containers show "Up" status, especially the `banking-app` container.

## 2. Check Application Logs

Check the logs of the banking-app container to see if there are any errors:

```bash
docker-compose logs banking-app
```

Look for any error messages related to binding, network, or database connections.

## 3. Check Network Configuration

### 3.1 Check if the application is listening on the correct port

```bash
docker-compose exec banking-app netstat -tulpn | grep 5000
```

You should see something like:
```
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      -
```

If you see `127.0.0.1:5000` instead of `0.0.0.0:5000`, the application is only binding to localhost inside the container.

### 3.2 Check if the port is exposed correctly

```bash
docker-compose exec banking-app cat /proc/1/cmdline | tr '\0' ' '
```

Make sure it shows `gunicorn --bind 0.0.0.0:5000 ...`

## 4. Check Firewall Settings

Check if the firewall is blocking port 5000:

```bash
sudo ufw status
```

If UFW is active, allow port 5000:

```bash
sudo ufw allow 5000/tcp
```

Also check iptables rules:

```bash
sudo iptables -L | grep 5000
```

If needed, add a rule to allow port 5000:

```bash
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
```

## 5. Test Internal Container Access

Check if the application is accessible from inside the container:

```bash
docker-compose exec banking-app curl -v http://localhost:5000/health
```

If this works but external access doesn't, it's likely a network or firewall issue.

## 6. Check Host Network Interface

Make sure the host is listening on the correct interface:

```bash
netstat -tulpn | grep 5000
```

You should see something like:
```
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      -
```

## 7. Restart the Application

If all else fails, try rebuilding and restarting the application:

```bash
# Make the restart script executable
chmod +x restart_services.sh

# Run the restart script
./restart_services.sh
```

## 8. Check Server IP Address

If you're trying to access the application from a different machine, make sure you're using the server's IP address instead of localhost:

```bash
# Get the server's IP address
ip addr show | grep inet

# Try accessing the application using the server's IP
curl http://SERVER_IP:5000/health
```

## 9. Additional Debugging

If the issue persists, try these additional debugging steps:

```bash
# Check if port 5000 is actually in use
sudo lsof -i :5000

# Check Docker network configuration
docker network ls
docker network inspect banking-network

# Check if the container's port is properly mapped
docker port banking-app
```

## 10. Temporary Solution: Use Host Network

If all else fails, you can modify the docker-compose.yml file to use the host network:

```yaml
banking-app:
  network_mode: "host"
  # Remove the ports section when using host network
```

This will make the container use the host's network stack directly, bypassing Docker's network isolation.