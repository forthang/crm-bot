from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    # Telegram
    BOT_TOKEN: SecretStr
    ADMIN_IDS: str  # Придет строкой "123,456", разберем позже
    
    # Security
    BOT_PASSWORD: SecretStr

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # AI
    OPENAI_API_KEY: SecretStr

    # Settings
    TIMEZONE: str = "UTC"

    # Магическая строка для чтения .env файла
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    @property
    def database_url(self) -> str:
        # Собираем ссылку для подключения к БД
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

# Инициализируем настройки
config = Settings()