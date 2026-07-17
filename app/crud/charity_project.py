"""CRUD-операции для целевых проектов."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """CRUD-класс целевых проектов."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> int | None:
        """Вернуть идентификатор проекта по имени."""
        return await session.scalar(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )


charity_project_crud = CRUDCharityProject(CharityProject)
