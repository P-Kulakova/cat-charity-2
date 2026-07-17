"""Валидаторы для API целевых проектов."""

from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


PROJECT_NAME_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_HAS_INVESTMENTS = (
    'В проект были внесены средства, не подлежит удалению!'
)
PROJECT_CLOSED = (
    'Закрытый проект нельзя изменить или удалить!'
)
FULL_AMOUNT_LESS_THAN_INVESTED = (
    'Требуемая сумма не может быть меньше уже вложенной в проект!'
)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверяет, что проекта с таким именем ещё нет."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session,
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NAME_EXISTS,
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Возвращает проект или выбрасывает 404, если он не найден."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND,
        )
    return project


def check_project_is_donated(
    project: CharityProject,
) -> CharityProject:
    """Запрещает удалять проект, в который уже внесены средства."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_HAS_INVESTMENTS,
        )
    return project


def check_project_is_closed(
    project: CharityProject,
) -> CharityProject:
    """Запрещает редактировать или удалять закрытый проект."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_CLOSED,
        )
    return project


def check_full_amount_more_than_invested(
    project: CharityProject,
    new_full_amount: int,
) -> CharityProject:
    """Проверяет, что новая требуемая сумма не меньше уже вложенной."""
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FULL_AMOUNT_LESS_THAN_INVESTED,
        )
    return project
