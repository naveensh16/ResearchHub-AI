# ResearchHub AI Setup Script (Windows PowerShell)

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "ResearchHub AI - Setup Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+!" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
}
else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null
Write-Host "✓ Pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "(This may take a few minutes)" -ForegroundColor Gray
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create .env file if not exists
Write-Host ""
Write-Host "Setting up environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file already exists" -ForegroundColor Yellow
}
else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created from template" -ForegroundColor Green
}

# Create uploads folder
Write-Host ""
Write-Host "Creating uploads folder..." -ForegroundColor Yellow
if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
    Write-Host "✓ Uploads folder created" -ForegroundColor Green
}
else {
    Write-Host "Uploads folder already exists" -ForegroundColor Yellow
}

# Check for Ollama (optional)
Write-Host ""
Write-Host "Checking for Ollama (local AI)..." -ForegroundColor Yellow
try {
    $ollamaCheck = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
    Write-Host "✓ Ollama is running!" -ForegroundColor Green
    Write-Host "  You can use local AI models" -ForegroundColor Gray
} catch {
    Write-Host "⚠ Ollama not detected" -ForegroundColor Yellow
    Write-Host "  Install Ollama for local AI: https://ollama.ai" -ForegroundColor Gray
    Write-Host "  Or configure OpenAI API key in .env file" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your configuration" -ForegroundColor White
Write-Host "2. Run: python run.py" -ForegroundColor White
Write-Host "3. Open: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "For AI features:" -ForegroundColor Yellow
Write-Host "  • Install Ollama + download mistral model" -ForegroundColor White
Write-Host "  • Or add OPENAI_API_KEY to .env" -ForegroundColor White
Write-Host ""
