# ResearchHub AI - Quick Start Script
# Activates environment and runs the application

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Starting ResearchHub AI..." -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "  Run setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Run the application
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host ""
python run.py
