from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
    redis_url: str = "redis://db-cache:6379/0"
    cookie_key: str = "access_token"
    cookie_secure: bool = False
    auth_api_url: str = "https://dauth.johnmgrubbs.io"
    frontend_url: str = "http://localhost:5173"
    frontend_origins: str | None = None
    admin_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
