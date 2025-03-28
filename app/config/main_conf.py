import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
]

def find_env_file():
    for path in ENV_PATHS:
        if os.path.exists(path):
            return path
    return None
class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    CHANNEL_ID: str
    MAX_GAMES_PER_DAY: int|None = 2
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    model_config = SettingsConfigDict(
        env_file=find_env_file(),
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore',
    )


settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
