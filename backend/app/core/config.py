"""Configuration settings for SustainMetric backend."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SustainMetric IDX Harness"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    DATABASE_URL: str = "postgresql+asyncpg://sustainmetric:sustainmetric_secret@127.0.0.1:5432/sustainmetric_db"
    SYNC_DATABASE_URL: str = "postgresql+pg8000://sustainmetric:sustainmetric_secret@127.0.0.1:5432/sustainmetric_db"
    
    # Sectors App Financials API
    SECTORS_API_KEY: str = ""
    CACHE_TTL_FINANCIALS_SEC: int = 604800  # 7 days
    CACHE_TTL_NEWS_SEC: int = 86400         # 24 hours
    
    # Multi-provider LLM API keys
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "nvidia/nemotron-3.5-lightning:free"
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"
    DEFAULT_LLM_PROVIDER: str = "openrouter"    # openrouter, gemini, openai, anthropic, ollama
    DEFAULT_LLM_MODEL: str = "nvidia/nemotron-3.5-lightning:free"
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ]
    
    # Telemetry
    ENABLE_OTEL_TRACING: bool = True
    OTEL_SERVICE_NAME: str = "sustainmetric-backend"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
