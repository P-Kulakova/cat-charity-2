"""Pydantic-схемы целевых проектов."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core.constants import (
    PROJECT_DESCRIPTION_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_NAME_MIN_LENGTH,
)


class CharityProjectBase(BaseModel):
    """Базовая схема целевого проекта."""

    name: str | None = Field(
        None,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH,
    )
    description: str | None = Field(
        None,
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH,
    )
    full_amount: PositiveInt | None = None


class CharityProjectCreate(CharityProjectBase):
    """Схема создания целевого проекта."""

    name: str = Field(
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH,
    )
    description: str = Field(min_length=PROJECT_DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt

    model_config = ConfigDict(extra='forbid')


class CharityProjectUpdate(CharityProjectBase):
    """Схема частичного обновления целевого проекта."""

    model_config = ConfigDict(extra='forbid')


class CharityProjectDB(CharityProjectCreate):
    """Схема целевого проекта в ответе API."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
