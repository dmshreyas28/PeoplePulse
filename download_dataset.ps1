# Quick Setup Script for IBM HR Dataset
# Run this after setting your Kaggle credentials

Write-Host "PeoplePulse - Kaggle Dataset Download Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Kaggle credentials are set
if (-not $env:KAGGLE_USERNAME -or -not $env:KAGGLE_KEY) {
    Write-Host "❌ Kaggle credentials not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set your Kaggle credentials first:" -ForegroundColor Yellow
    Write-Host '  $env:KAGGLE_USERNAME = "your_username"' -ForegroundColor White
    Write-Host '  $env:KAGGLE_KEY = "your_api_key"' -ForegroundColor White
    Write-Host ""
    Write-Host "Get your API key from: https://www.kaggle.com/settings" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "✓ Kaggle credentials found" -ForegroundColor Green
Write-Host ""

# Create data directory if it doesn't exist
$dataDir = "e:\PeoplePulse\data\raw"
if (-not (Test-Path $dataDir)) {
    Write-Host "Creating data directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
}

Write-Host "Downloading IBM HR Analytics dataset from Kaggle..." -ForegroundColor Yellow
Write-Host ""

# Download the dataset
try {
    Set-Location "e:\PeoplePulse\ml"
    .\.venv\Scripts\kaggle datasets download -d pavansubhasht/ibm-hr-analytics-attrition-dataset -p ../data/raw --unzip
    
    Write-Host ""
    Write-Host "✓ Dataset downloaded successfully!" -ForegroundColor Green
    Write-Host ""
    
    # Check if file exists and show info
    $csvFile = Get-ChildItem -Path $dataDir -Filter "*.csv" | Select-Object -First 1
    if ($csvFile) {
        Write-Host "Dataset file: $($csvFile.FullName)" -ForegroundColor Cyan
        Write-Host "File size: $([math]::Round($csvFile.Length / 1KB, 2)) KB" -ForegroundColor Cyan
        
        # Count rows
        $lineCount = (Get-Content $csvFile.FullName | Measure-Object -Line).Lines
        Write-Host "Total rows: $($lineCount - 1) (excluding header)" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "✓ Ready to train! Run:" -ForegroundColor Green
        Write-Host "  cd e:\PeoplePulse\ml" -ForegroundColor White
        Write-Host "  .\.venv\Scripts\python pipeline/train.py --config pipeline/config.yaml" -ForegroundColor White
    }
}
catch {
    Write-Host ""
    Write-Host "❌ Error downloading dataset: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "You can manually download from:" -ForegroundColor Yellow
    Write-Host "  https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset" -ForegroundColor White
    exit 1
}
