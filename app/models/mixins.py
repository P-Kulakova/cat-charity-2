"""Mixin-ы ORM-моделей."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column


class InvestmentMixin:
    """Общие поля для инвестируемых объектов."""

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    close_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
