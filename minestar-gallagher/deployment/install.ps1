# Run as Administrator
Write-Host "Installing MineStar-Gallagher Service..." -ForegroundColor Green

# Create directories
New-Item -ItemType Directory -Force -Path "C:\ProgramData\SEME\MineStarGallagher\data"
New-Item -ItemType Directory -Force -Path "C:\ProgramData\SEME\MineStarGallagher\logs"
New-Item -ItemType Directory -Force -Path "C:\ProgramData\SEME\MineStarGallagher\backup"

# Install service
python run_service.py install

Write-Host "Service installed. Use: python run_service.py start" -ForegroundColor Green