from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ================== REQUIRED FOR TESTING ==================
    gallagher_api_key: str = "sk_test_XXXXXXXXXXXXXXXXXXXXXXXX"   # ← Your Gallagher API key

    mine_star_sql_connection: str = (
        "DRIVER={SQL Server};"
        "SERVER=localhost;"                    # ← localhost as requested
        "DATABASE=YourMineStarDBName;"
        "UID=your_sql_login;"
        "PWD=your_sql_password;"
        "TrustServerCertificate=yes;"
    )
    # ========================================================

    # Gallagher REST endpoint - localhost only
    gallagher_base_url: str = "https://localhost:8904"   # ← Default Gallagher REST port

    environment: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()