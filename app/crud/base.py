"""Базовый CRUD-класс для работы с ORM-моделями."""

from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


ModelType = TypeVar('ModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType]):
    """Общие CRUD-операции для моделей SQLAlchemy."""

    def __init__(self, model: type[ModelType]) -> None:
        """Сохраняет модель, с которой будет работать CRUD-объект."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> ModelType | None:
        """Вернуть объект по идентификатору."""
        return await session.get(self.model, obj_id)

    async def get_multi(self, session: AsyncSession) -> list[ModelType]:
        """Возвращает список всех объектов модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: SchemaType,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        """Создаёт объект модели и при необходимости сразу сохраняет его."""
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.flush()
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: SchemaType,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        """Обновить объект переданными полями."""
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Удаляет объект из базы данных."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        """Вернуть открытые объекты в порядке их создания и id."""
        db_objs = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date, self.model.id)
        )
        return db_objs.scalars().all()
