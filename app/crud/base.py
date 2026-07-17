"""Базовый CRUD-класс для работы с ORM-моделями."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Общие CRUD-операции для моделей SQLAlchemy."""

    def __init__(self, model):
        """Сохраняет модель, с которой будет работать CRUD-объект."""
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        """Вернуть объект по идентификатору."""
        return await session.get(self.model, obj_id)

    async def get_multi(self, session: AsyncSession):
        """Возвращает список всех объектов модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession, commit: bool = True):
        """Создаёт объект модели и при необходимости сразу сохраняет его."""
        obj_data = obj_in.model_dump()
        if hasattr(self.model, 'invested_amount'):
            obj_data.setdefault('invested_amount', 0)
        if hasattr(self.model, 'fully_invested'):
            obj_data.setdefault('fully_invested', False)
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
        commit: bool = True,
    ):
        """Обновить объект переданными полями."""
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession):
        """Удаляет объект из базы данных."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ):
        """Вернуть открытые объекты в порядке их создания и id."""
        db_objs = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date, self.model.id)
        )
        return db_objs.scalars().all()
