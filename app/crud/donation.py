"""CRUD операции для пожертвований."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation]):
    """CRUD операции для пожертвований."""

    async def create(
        self,
        obj_in: DonationCreate,
        session: AsyncSession,
        user: User | None = None,
        commit: bool = True,
    ) -> Donation:
        """Создать пожертвование, при наличии привязав его к пользователю."""
        obj_data = obj_in.model_dump()
        if user is not None:
            obj_data['user_id'] = user.id
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.flush()
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get_by_user(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> list[Donation]:
        """Возвращает пожертвования, созданные конкретным пользователем."""
        db_objs = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
