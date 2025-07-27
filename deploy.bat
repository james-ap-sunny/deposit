@echo off
REM One-click deployment script for Core Banking Transfer System (Windows)

echo === Core Banking Transfer System Deployment ===
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop for Windows from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not available
    echo Please ensure Docker Desktop is properly installed
    pause
    exit /b 1
)

echo [INFO] Docker and Docker Compose are available

REM Create .env file if it doesn't exist
if not exist .env (
    echo [INFO] Creating .env file...
    copy .env.example .env
    echo [INFO] .env file created. Please review and update passwords if needed.
)

REM Create logs directory
if not exist logs mkdir logs

echo [INFO] Setting up environment...

REM Stop any existing containers
echo [INFO] Stopping existing containers...
docker-compose down --remove-orphans

REM Pull latest images
echo [INFO] Pulling Docker images...
docker-compose pull

REM Build application image
echo [INFO] Building application image...
docker-compose build banking-app

REM Start services
echo [INFO] Starting services...
docker-compose up -d

REM Wait for services to start
echo [INFO] Waiting for services to start (30 seconds)...
timeout /t 30 /nobreak >nul

REM Check application health
echo [INFO] Checking application health...
for /l %%i in (1,1,10) do (
    curl -f http://localhost:5000/health >nul 2>&1
    if !errorlevel! equ 0 (
        echo [INFO] Application is healthy!
        goto :health_ok
    )
    echo [INFO] Waiting for application to be ready... (attempt %%i/10)
    timeout /t 10 /nobreak >nul
)

echo [ERROR] Application health check failed after 10 attempts.
echo [ERROR] Check logs with: docker-compose logs banking-app
goto :end

:health_ok
echo.
echo === Deployment Information ===
echo.
echo 🏦 Core Banking Transfer System is now running!
echo.
echo 📊 Service URLs:
echo    • Application API: http://localhost:5000
echo    • Health Check: http://localhost:5000/health
echo    • Detailed Health: http://localhost:5000/health/detailed
echo.
echo 🗄️  Database Ports:
echo    • Source Database (MySQL): localhost:3306
echo    • Destination Database (MySQL): localhost:3307
echo    • Redis Cache: localhost:6379
echo.
echo 🔧 Management Commands:
echo    • View logs: docker-compose logs -f
echo    • Stop services: docker-compose down
echo    • Restart services: docker-compose restart
echo    • View status: docker-compose ps
echo.
echo 📋 Sample API Calls:
echo    • Get account info: curl http://localhost:5000/api/v1/accounts/6230399991006371427
echo    • Create transfer: curl -X POST http://localhost:5000/api/v1/transfers ^
echo      -H "Content-Type: application/json" ^
echo      -d "{\"from_account\":\"6230399991006371427\",\"to_account\":\"6230399991006371430\",\"amount\":100.00}"
echo.
echo [INFO] Deployment completed successfully! 🎉

:end
pause