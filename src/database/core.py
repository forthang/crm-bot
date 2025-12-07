from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import config
from src.database.models import Base

# Create an asynchronous engine
engine = create_async_engine(
    url=config.database_url,
    echo=False  # Set to True to see SQL queries in the console
)

# Session factory (for making queries)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    """Creates tables in the DB on startup if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)