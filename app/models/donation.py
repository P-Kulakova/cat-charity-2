"""Модель пожертвования."""

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin
from app.models.mixins import InvestmentMixin


class Donation(InvestmentMixin, CommonMixin, Base):
    """Модель пожертвования."""

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
    )

    def __repr__(self):
        """Возвращает строковое представление пожертвования."""
        return (
            f'{self.__class__.__name__}('
            f'id={self.id!r}, '
            f'full_amount={self.full_amount!r}, '
            f'invested_amount={self.invested_amount!r}, '
            f'comment={self.comment!r}, '
            f'user_id={self.user_id!r})'
        )
