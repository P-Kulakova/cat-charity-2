"""ORM-модель целевого проекта."""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import PROJECT_NAME_MAX_LENGTH
from app.core.db import Base, CommonMixin
from app.models.mixins import InvestmentMixin


class CharityProject(InvestmentMixin, CommonMixin, Base):
    """Целевой проект для сбора пожертвований."""

    name: Mapped[str] = mapped_column(
        String(PROJECT_NAME_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        """Возвращает строковое представление проекта."""
        return (
            f'{self.__class__.__name__}('
            f'name={self.name!r}, '
            f'full_amount={self.full_amount!r}, '
            f'invested_amount={self.invested_amount!r})'
        )
