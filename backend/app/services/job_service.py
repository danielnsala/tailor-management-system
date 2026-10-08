from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.payment import Payment
from app.schemas.order import JobUpdate


class InvalidJobPriceError(Exception):
    pass


class JobService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def update_job(
        self,
        order_id: int,
        job_id: int,
        job_update: JobUpdate,
    ) -> Job | None:
        job = self.db_session.execute(
            select(Job).where(
                Job.id == job_id,
                Job.order_id == order_id,
            )
        ).scalar_one_or_none()
        if job is None:
            return None

        update_data = job_update.model_dump(exclude_unset=True, exclude_none=True)
        proposed_price = update_data.get("price")

        if proposed_price is not None and proposed_price != job.price:
            total = self.db_session.scalar(
                select(func.sum(Job.price)).where(Job.order_id == order_id)
            ) or Decimal("0.00")
            paid = self.db_session.scalar(
                select(func.sum(Payment.amount)).where(Payment.order_id == order_id)
            ) or Decimal("0.00")
            proposed_total = total - job.price + proposed_price

            if proposed_total < paid:
                raise InvalidJobPriceError(
                    f"Updated order total of ${proposed_total:.2f} is less than "
                    f"the ${paid:.2f} already paid"
                )

        for field, value in update_data.items():
            setattr(job, field, value)

        self.db_session.commit()
        self.db_session.refresh(job)
        return job

    