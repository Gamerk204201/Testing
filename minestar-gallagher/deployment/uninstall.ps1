# Run as Administrator
Write-Host "Uninstalling MineStar-Gallagher Service..." -ForegroundColor Yellow

# Stop and uninstall the service
python run_service.py stop
python run_service.py remove

Write-Host "Service uninstalled successfully." -ForegroundColor Green
Write-Host "You can delete the application folder if needed." -ForegroundColor Gray