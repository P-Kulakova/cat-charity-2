"""Эндпоинты для работы с целевыми проектами."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_full_amount_more_than_invested,
    check_name_duplicate,
    check_project_is_closed,
    check_project_is_donated,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import close_if_fully_invested, invest_new_object


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
):
    """Создаёт проект и распределяет в него свободные пожертвования.
    Только для суперпользователей.
    """
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project,
        session,
        commit=False,
    )
    donations = await donation_crud.get_not_fully_invested(session)
    invest_new_object(new_project, donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_charity_projects(session: SessionDep):
    """Возвращает список всех целевых проектов.
    Доступно без авторизации.
    """
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: SessionDep,
):
    """Частично обновляет целевой проект.
    Только для суперпользователей.
    """
    db_project = await check_charity_project_exists(project_id, session)
    check_project_is_closed(db_project)
    if charity_project.name is not None:
        await check_name_duplicate(charity_project.name, session)
    if charity_project.full_amount is not None:
        check_full_amount_more_than_invested(
            db_project,
            charity_project.full_amount,
        )
    db_project = await charity_project_crud.update(
        db_project,
        charity_project,
        session,
        commit=False,
    )
    close_if_fully_invested(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    """Удаляет проект, если он не закрыт и в него не внесены средства.
    Только для суперпользователей.
    """
    db_project = await check_charity_project_exists(project_id, session)
    check_project_is_donated(db_project)
    check_project_is_closed(db_project)
    return await charity_project_crud.remove(db_project, session)
