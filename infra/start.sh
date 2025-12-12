#!/bin/bash

# PeoplePulse - Quick Start Script

echo "🚀 Starting PeoplePulse platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Navigate to infra directory
cd infra

# Build and start all services
echo "📦 Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend API is running at http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
else
    echo "⚠️  Backend API is not responding yet"
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "⚠️  Frontend is not responding yet"
fi

# Check database
if docker exec peoplepulse-db pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ Database is running"
else
    echo "⚠️  Database is not ready yet"
fi

# Check MLflow
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ MLflow is running at http://localhost:5000"
else
    echo "⚠️  MLflow is not responding yet"
fi

echo ""
echo "🎉 PeoplePulse is starting up!"
echo ""
echo "📊 Access points:"
echo "   Frontend Dashboard: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   MLflow UI: http://localhost:5000"
echo "   PgAdmin: http://localhost:5050 (admin@peoplepulse.com / admin)"
echo ""
echo "⚠️  Note: Model training is required before predictions will work."
echo "   Run: python ml/pipeline/train.py --config ml/pipeline/config.yaml"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
