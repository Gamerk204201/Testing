# Deployment Guide

## Production Location
C:\Program Files\SEME\MineStarGallagher\

## Steps

1. Copy application folder
2. Create data directory in ProgramData
3. Configure .env
4. Install service: `python run_service.py install`
5. Start service: `python run_service.py start`

## Rollback
Run `rollback.ps1`

## Uninstall
Run `uninstall.ps1`