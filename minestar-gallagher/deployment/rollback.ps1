Write-Host "Rolling back service..." -ForegroundColor Red
python run_service.py stop
# Add backup restore logic here later
python run_service.py start