from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

connection = create_async_engine(settings.DATABASE_URL, echo=False)
main_session = async_sessionmaker(connection, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with main_session() as session:
        yield session