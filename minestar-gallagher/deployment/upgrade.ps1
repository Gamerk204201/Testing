Write-Host "Upgrading service..." -ForegroundColor Yellow
python run_service.py stop
python run_service.py install
python run_service.py start
Write-Host "Upgrade complete" -ForegroundColor Green