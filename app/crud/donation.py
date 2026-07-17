"""CRUD операции для пожертвований."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    """CRUD операции для пожертвований."""

    async def get_by_user(
        self,
        user_id: int,
        session: AsyncSession,
    ):
        """Возвращает пожертвования, созданные конкретным пользователем."""
        db_objs = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
