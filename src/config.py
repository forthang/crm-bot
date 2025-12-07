from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):

    # Telegram

    BOT_TOKEN: SecretStr

    ADMIN_IDS: str  # Comes as a string "123,456", will be parsed later

    

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



    # Magic string to read the .env file

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')



    @property

    def database_url(self) -> str:

        # Assemble the database connection link

        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"

                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")



# Initialize settings

config = Settings()
