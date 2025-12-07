from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import config
from src.database.models import Base

# Создаем асинхронный движок
engine = create_async_engine(
    url=config.database_url,
    echo=False  # Поставь True, если хочешь видеть SQL запросы в консоли
)

# Фабрика сессий (через нее будем делать запросы)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    """Создает таблицы в БД при запуске, если их нет"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)