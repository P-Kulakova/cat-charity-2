"""Сервис распределения пожертвований по целевым проектам."""

from collections.abc import Iterable
from datetime import datetime

from app.models.charity_project import CharityProject
from app.models.donation import Donation


InvestmentObject = CharityProject | Donation


def close_if_fully_invested(
    obj: InvestmentObject,
    close_date: datetime | None = None,
) -> None:
    """Закрывает объект, если он полностью инвестирован."""
    if (
        obj.invested_amount >= obj.full_amount
        and not obj.fully_invested
    ):
        obj.fully_invested = True
        obj.close_date = close_date or datetime.now()


def invest_new_object(
    target: InvestmentObject,
    sources: Iterable[InvestmentObject],
) -> None:
    """Распределяет свободную сумму нового объекта по открытым объектам."""
    close_date = datetime.now()

    for source in sources:
        target_free = target.full_amount - target.invested_amount
        source_free = source.full_amount - source.invested_amount

        invested_amount = min(target_free, source_free)

        target.invested_amount += invested_amount
        source.invested_amount += invested_amount

        close_if_fully_invested(target, close_date)
        close_if_fully_invested(source, close_date)

        if target.fully_invested:
            break
