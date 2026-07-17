"""Схемы пожертвований."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveInt


class DonationCreate(BaseModel):
    """Схема создания пожертвования."""

    full_amount: PositiveInt
    comment: str | None = None

    model_config = ConfigDict(extra='forbid')


class DonationDB(DonationCreate):
    """Краткая схема пожертвования для ответа пользователю."""

    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    """Полная схема пожертвования для суперпользователя."""

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None = None
