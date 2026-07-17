"""Эндпоинты для работы с пожертвованиями."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest_new_object


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
UserDep = Annotated[User, Depends(current_user)]
SuperuserDep = Annotated[User, Depends(current_superuser)]


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: UserDep,
):
    """Сделать пожертвование.
    Только для зарегистрированных пользователей.
    """
    new_donation = await donation_crud.create(donation, session, commit=False)
    new_donation.user_id = user.id
    projects = await charity_project_crud.get_not_fully_invested(session)
    invest_new_object(new_donation, projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(session: SessionDep, user: UserDep):
    """Показать список пожертвований пользователя, выполняющего запрос.
    Только для зарегистрированных пользователей.
    """
    return await donation_crud.get_by_user(user.id, session)


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: SessionDep,
    superuser: SuperuserDep,
):
    """Показать список всех пожертвований.
    Только для суперюзеров.
    """
    return await donation_crud.get_multi(session)
