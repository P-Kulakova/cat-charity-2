"""Эндпоинты регистрации, аутентификации и управления пользователями."""

from fastapi import APIRouter, HTTPException, status

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter()

auth_router = fastapi_users.get_auth_router(auth_backend)
router.include_router(
    auth_router,
    prefix='/auth/jwt',
    tags=['auth'],
)

register_router = fastapi_users.get_register_router(UserRead, UserCreate)
router.include_router(
    register_router,
    prefix='/auth',
    tags=['auth'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)


@router.delete('/users/{user_id}', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
async def delete_user_forbidden(user_id: str):
    """Запрещает удаление пользователей."""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail='Удаление пользователей запрещено.',
    )


router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)
