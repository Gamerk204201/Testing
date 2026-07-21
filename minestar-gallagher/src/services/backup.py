import shutil
from datetime import datetime

def backup_database():
    """Simple backup"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    shutil.copy(
        "C:/ProgramData/SEME/MineStarGallagher/data/integration.db",
        f"C:/ProgramData/SEME/MineStarGallagher/backup/integration_{timestamp}.db"
    )
    print(f"Backup created: integration_{timestamp}.db")