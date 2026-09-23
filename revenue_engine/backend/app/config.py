from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Amravati Revenue Engine"
    environment: str = "development"
    debug: bool = True
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./revenue_engine.db"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:5173","http://localhost:3000"]
    outreach_dry_run: bool = True
    max_outreach_per_hour: int = 50
    upi_vpa: str = ""
    upi_payee_name: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
