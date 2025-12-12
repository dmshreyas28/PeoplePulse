# PeoplePulse - Quick Start Script (PowerShell)

Write-Host "🚀 Starting PeoplePulse platform..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Navigate to infra directory
Set-Location infra

# Build and start all services
Write-Host "📦 Building and starting services..." -ForegroundColor Yellow
docker-compose up --build -d

Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Yellow

# Check backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Backend API is running at http://localhost:8000" -ForegroundColor Green
    Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  Backend API is not responding yet" -ForegroundColor Yellow
}

# Check frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Frontend is running at http://localhost:3000" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Frontend is not responding yet" -ForegroundColor Yellow
}

# Check database
try {
    docker exec peoplepulse-db pg_isready -U postgres | Out-Null
    Write-Host "✅ Database is running" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Database is not ready yet" -ForegroundColor Yellow
}

# Check MLflow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ MLflow is running at http://localhost:5000" -ForegroundColor Green
} catch {
    Write-Host "⚠️  MLflow is not responding yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 PeoplePulse is starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Access points:" -ForegroundColor Cyan
Write-Host "   Frontend Dashboard: http://localhost:3000"
Write-Host "   Backend API: http://localhost:8000"
Write-Host "   API Documentation: http://localhost:8000/docs"
Write-Host "   MLflow UI: http://localhost:5000"
Write-Host "   PgAdmin: http://localhost:5050 (admin@peoplepulse.com / admin)"
Write-Host ""
Write-Host "⚠️  Note: Model training is required before predictions will work." -ForegroundColor Yellow
Write-Host "   Run: python ml/pipeline/train.py --config ml/pipeline/config.yaml"
Write-Host ""
Write-Host "To view logs: docker-compose logs -f"
Write-Host "To stop: docker-compose down"
