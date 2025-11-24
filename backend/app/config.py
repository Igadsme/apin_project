from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "APIN Backend"
    database_url: str = "sqlite:///./apin.db"

    class Config:
        env_file = ".env"


settings = Settings()
