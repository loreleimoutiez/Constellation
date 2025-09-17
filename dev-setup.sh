#!/bin/bash
# Constellation CMDB - Quick Development Setup Script

set -e

echo "🌟 Constellation CMDB - Development Setup"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. You can modify it as needed."
fi

# Build containers
echo ""
echo "🔧 Building Docker containers..."
if docker compose version >/dev/null 2>&1; then
    docker compose build --no-cache
else
    docker-compose build --no-cache
fi

# Start services
echo ""
echo "🚀 Starting Constellation services..."
if docker compose version >/dev/null 2>&1; then
    docker compose up -d neo4j api
else
    docker-compose up -d neo4j api
fi

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service health..."

# Check Neo4j
if curl -s -f http://localhost:7474 >/dev/null; then
    echo "✅ Neo4j is running at http://localhost:7474"
    echo "   Username: neo4j"
    echo "   Password: constellation123"
else
    echo "⚠️  Neo4j might still be starting up..."
fi

# Check API
if curl -s -f http://localhost:8000/docs >/dev/null; then
    echo "✅ FastAPI is running at http://localhost:8000/docs"
else
    echo "⚠️  FastAPI might still be starting up..."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Quick Links:"
echo "  📊 Neo4j Browser: http://localhost:7474"
echo "  📚 API Documentation: http://localhost:8000/docs"
echo "  📋 API Health Check: http://localhost:8000/health"
echo ""
echo "Useful Commands:"
echo "  make logs       # View all logs"
echo "  make shell-api  # Shell access to API container"
echo "  make down       # Stop all services"
echo "  make clean      # Stop and clean up"
echo ""
echo "🚀 Happy coding!"