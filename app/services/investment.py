"""Сервис распределения пожертвований по целевым проектам."""

from datetime import datetime


def close_if_fully_invested(obj, close_date=None):
    """Закрывает объект, если он полностью инвестирован."""
    if (
        obj.invested_amount >= obj.full_amount
        and not obj.fully_invested
    ):
        obj.fully_invested = True
        obj.close_date = close_date or datetime.now()


def invest_new_object(target, sources):
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

    return target
