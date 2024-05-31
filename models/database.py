import asyncio
from sqlalchemy.ext.asyncio import (AsyncSession, create_async_engine,
                                    async_sessionmaker)
from sqlalchemy.orm import sessionmaker, declarative_base
from models.models import User, Base
# DATABASE_URL = "sqlite:///users_sqlite.db"
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# async def get_session() -> AsyncSession:
#     """context manager for automatic open and close db session"""
#     async with async_session() as session:
#         yield session


