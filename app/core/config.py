from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Сюда будет подставляться строка из .env

    class Config:
        env_file = ".env"  # Указываем, откуда брать переменные окружения

# Создаем объект настроек
settings = Settings()
