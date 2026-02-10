@echo off
echo ====================================================
echo 🎰 Lottery Investment Calculator - Docker Setup
echo ====================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo    Download: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo ✅ Docker is installed and running
echo.

REM Build images
echo 🏗️  Building Docker images...
echo    This may take 5-10 minutes on first run (downloading browsers, etc.)
echo.
docker-compose build

if %errorlevel% neq 0 (
    echo ❌ Build failed. Check the errors above.
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo.

REM Start containers
echo 🚀 Starting containers...
docker-compose up -d

if %errorlevel% neq 0 (
    echo ❌ Failed to start containers.
    pause
    exit /b 1
)

echo.
echo ✅ All containers started successfully!
echo.
echo ====================================================
echo 🌐 Your application is now running:
echo ====================================================
echo.
echo    Frontend:  http://localhost:3003
echo    Backend:   http://localhost:5000
echo    Health:    http://localhost:5000/api/health
echo.
echo ====================================================
echo 📊 Useful commands:
echo ====================================================
echo.
echo    View logs:        docker-compose logs -f
echo    Stop:             docker-compose down
echo    Restart:          docker-compose restart
echo    Rebuild:          docker-compose up -d --build
echo.
echo 📖 See DOCKER_README.md for full documentation
echo.
pause
