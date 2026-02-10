#!/bin/bash

echo "🎰 Lottery Investment Calculator - Docker Setup"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Download: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Build images
echo "🏗️  Building Docker images..."
echo "   This may take 5-10 minutes on first run (downloading browsers, etc.)"
echo ""
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Check the errors above."
    exit 1
fi

echo ""
echo "✅ Build completed successfully!"
echo ""

# Start containers
echo "🚀 Starting containers..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start containers."
    exit 1
fi

echo ""
echo "✅ All containers started successfully!"
echo ""
echo "================================================"
echo "🌐 Your application is now running:"
echo "================================================"
echo ""
echo "   Frontend:  http://localhost:3003"
echo "   Backend:   http://localhost:5000"
echo "   Health:    http://localhost:5000/api/health"
echo ""
echo "================================================"
echo "📊 Useful commands:"
echo "================================================"
echo ""
echo "   View logs:        docker-compose logs -f"
echo "   Stop:             docker-compose down"
echo "   Restart:          docker-compose restart"
echo "   Rebuild:          docker-compose up -d --build"
echo ""
echo "📖 See DOCKER_README.md for full documentation"
echo ""
