from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ------------------------------------------------------------------
    # Gallagher
    # ------------------------------------------------------------------
    gallagher_api_key: str = "sk_test_XXXXXXXXXXXXXXXXXXXXXXXX"   # ← put your real key here
    gallagher_base_url: str = "https://localhost:8904"
    gallagher_verify_ssl: bool = False          # set True once you have proper certificates

    # ------------------------------------------------------------------
    # Dry-run mode (no real Gallagher calls)
    # ------------------------------------------------------------------
    dry_run: bool = False                       # True = log only, False = real API calls

    # ------------------------------------------------------------------
    # MineStar (fill in later when you get VM access)
    # ------------------------------------------------------------------
    mine_star_sql_connection: str = (
        "DRIVER={SQL Server};"
        "SERVER=localhost;"
        "DATABASE=YourMineStarDBName;"
        "UID=your_sql_login;"
        "PWD=your_sql_password;"
        "TrustServerCertificate=yes;"
    )

    # ------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------
    environment: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()