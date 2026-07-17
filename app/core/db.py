"""Базовые объекты SQLAlchemy и зависимость сессии."""

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""


class CommonMixin:
    """Общий mixin с именем таблицы и id."""

    @declared_attr
    def __tablename__(cls):
        """Возвращает имя таблицы по имени модели."""
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    """Предоставляет асинхронную сессию."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
