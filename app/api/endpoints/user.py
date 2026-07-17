"""Эндпоинты регистрации, аутентификации и управления пользователями."""

from fastapi import APIRouter

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
register_router.__doc__ = 'Регистрация нового пользователя. Доступно всем.'
router.include_router(
    register_router,
    prefix='/auth',
    tags=['auth'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes if route.name != 'users:delete_user'
]
router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)
