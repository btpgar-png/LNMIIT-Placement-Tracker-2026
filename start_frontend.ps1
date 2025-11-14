    Write-Host "Starting Frontend Development Server..." -ForegroundColor Cyan
Set-Location frontend

# Install dependencies if needed
if (-Not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Run the server
Write-Host "Starting server..." -ForegroundColor Green
npm start


