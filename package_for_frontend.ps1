# Simple PowerShell Script to Package Backend for Frontend Developer

Write-Host "Packaging backend for React frontend..." -ForegroundColor Cyan

# Create package directory
$packageDir = "bizviz-backend-package"
if (Test-Path $packageDir) {
    Remove-Item -Recurse -Force $packageDir
}
New-Item -ItemType Directory -Force -Path $packageDir | Out-Null

# Copy files
Write-Host "Copying services folder..."
Copy-Item -Path "services" -Destination "$packageDir\" -Recurse

Write-Host "Copying utils folder..."
Copy-Item -Path "utils" -Destination "$packageDir\" -Recurse

Write-Host "Copying API file..."
Copy-Item -Path "flask_api.py" -Destination "$packageDir\"

Write-Host "Copying configuration files..."
Copy-Item -Path "requirements.txt" -Destination "$packageDir\"
Copy-Item -Path ".env.example" -Destination "$packageDir\"

Write-Host "Copying test datasets..."
Get-ChildItem -Path "test_data_*.csv" | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination "$packageDir\"
}

Write-Host "Copying documentation..."
Copy-Item -Path "API_INTEGRATION_GUIDE.md" -Destination "$packageDir\"
Copy-Item -Path "SEND_TO_FRONTEND_DEV.md" -Destination "$packageDir\"
Copy-Item -Path "FRONTEND_INTEGRATION_CHECKLIST.md" -Destination "$packageDir\"
Copy-Item -Path "SEND_TO_FRIEND.md" -Destination "$packageDir\" -ErrorAction SilentlyContinue

# Create simple README
$readme = @"
# BizViz Backend - Ready for React Integration

## Quick Start

1. Install dependencies:
   pip install -r requirements.txt

2. Run API server:
   python flask_api.py

3. Test API:
   curl http://localhost:5000/api/health

## Documentation

- START HERE: SEND_TO_FRONTEND_DEV.md
- API DOCS: API_INTEGRATION_GUIDE.md  
- CHECKLIST: FRONTEND_INTEGRATION_CHECKLIST.md

## What You Get

- 5 REST API endpoints
- AI-powered chart recommendations
- Automatic data analysis and insights
- Interactive Plotly charts
- PNG export capability
- Complete documentation with React examples
- Test datasets included

Ready to build! See SEND_TO_FRONTEND_DEV.md to get started.
"@

Set-Content -Path "$packageDir\README.md" -Value $readme

# Create ZIP file
Write-Host "Creating ZIP file..."
$zipFile = "bizviz-backend-for-react.zip"
if (Test-Path $zipFile) {
    Remove-Item -Force $zipFile
}
Compress-Archive -Path "$packageDir\*" -DestinationPath $zipFile

Write-Host ""
Write-Host "SUCCESS! Package created: $zipFile" -ForegroundColor Green
Write-Host ""
Write-Host "Send this ZIP file to your frontend developer"
Write-Host "They should start with: SEND_TO_FRONTEND_DEV.md"
Write-Host ""
