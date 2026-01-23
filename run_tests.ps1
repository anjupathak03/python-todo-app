# PowerShell script to run tests with Keploy
param(
    [Parameter(Mandatory=$false)]
    [string]$Mode = "record"  # "record" or "test"
)

Write-Host "Python Todo App - Keploy Testing Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check if in correct directory
if (!(Test-Path "app.py")) {
    Write-Host "Error: Please run this script from the python-todo-app directory" -ForegroundColor Red
    exit 1
}

# Check if dependencies installed
Write-Host "`nChecking Python dependencies..." -ForegroundColor Yellow
$pipList = pip list
if (!($pipList -match "Flask")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

if ($Mode -eq "record") {
    Write-Host "`nMode: RECORD - Recording database calls" -ForegroundColor Green
    Write-Host "Make sure MySQL is running: docker-compose up -d" -ForegroundColor Yellow
    Write-Host ""
    
    # Check if Docker is running
    $dockerRunning = docker ps 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: Docker doesn't seem to be running. Starting MySQL..." -ForegroundColor Yellow
        docker-compose up -d
        Start-Sleep -Seconds 10
    }
    
    Write-Host "Recording tests with Keploy..." -ForegroundColor Cyan
    keploy mock-record -c "python -m pytest test_app.py -v" --path ./keploy
    
} elseif ($Mode -eq "test") {
    Write-Host "`nMode: TEST - Replaying mocked database calls" -ForegroundColor Green
    Write-Host "No database needed for this mode!" -ForegroundColor Yellow
    Write-Host ""
    
    # Check if mocks exist
    if (!(Test-Path "keploy")) {
        Write-Host "Error: No mocks found. Please run in 'record' mode first:" -ForegroundColor Red
        Write-Host "  .\run_tests.ps1 -Mode record" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Running tests with Keploy mocks..." -ForegroundColor Cyan
    keploy mock-test -c "python -m pytest test_app.py -v" --path ./keploy
    
} else {
    Write-Host "Invalid mode: $Mode" -ForegroundColor Red
    Write-Host "Usage: .\run_tests.ps1 -Mode [record|test]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  record - Record database calls (needs MySQL running)"
    Write-Host "  test   - Run tests with mocked calls (no database needed)"
    exit 1
}

Write-Host "`nDone!" -ForegroundColor Green
