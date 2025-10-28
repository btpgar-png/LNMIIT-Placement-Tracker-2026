from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    ADMIN_TOKEN is used to authorize admin-only endpoints.
    Set environment variable ADMIN_TOKEN or place it in backend/.env
    """

    ADMIN_TOKEN: str = "change-me"

    # Ensure values are loaded from backend/.env as well as process env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()  # type: ignore[arg-type]
