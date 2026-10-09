from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.payment import Payment
from app.schemas.order import JobCreate, JobUpdate
from app.models.order import Order
from app.models.enums import OrderStatus


class InvalidJobPriceError(Exception):
    pass

class OrderNotEditableError(Exception):
    pass

class JobDeletionError(Exception):
    pass

class JobService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_job(
        self,
        order_id: int,
        job_create: JobCreate,
    ) -> Job | None:

        order = self.db_session.get(Order, order_id)

        if order is None:
            return None

        if order.status in (
            OrderStatus.COMPLETED,
            OrderStatus.CANCELLED,
        ):
            raise OrderNotEditableError(
                "Cannot add jobs to completed or cancelled orders"
            )

        new_job = Job(
            order_id=order_id,
            **job_create.model_dump(),
        )

        self.db_session.add(new_job)
        self.db_session.commit()
        self.db_session.refresh(new_job)

        return new_job

    def get_jobs(self, order_id: int) -> list[Job] | None:
        order = self.db_session.get(Order, order_id)

        if order is None:
            return None

        return list(
            self.db_session.scalars(
                select(Job)
                .where(Job.order_id == order_id)
                .order_by(Job.id)
            ).all()
        )

    def get_job(self, order_id: int, job_id: int) -> Job | None:
        return self.db_session.scalar(
            select(Job).where(
                Job.id == job_id,
                Job.order_id == order_id,
            )
        )

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

        order = self.db_session.get(Order, order_id)

        if order is None:
            return None

        if order.status in (
            OrderStatus.COMPLETED,
            OrderStatus.CANCELLED,
        ):
            raise OrderNotEditableError(
                "Cannot update jobs in completed or cancelled orders"
            )

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

    def delete_job(
        self,
        order_id: int,
        job_id: int,
    ) -> bool:

        order = self.db_session.get(Order, order_id)

        if order is None:
            return False

        job = self.get_job(order_id, job_id)

        if job is None:
            return False

        if order.status in (
            OrderStatus.COMPLETED,
            OrderStatus.CANCELLED,
        ):
            raise OrderNotEditableError(
                "Cannot delete jobs from completed or cancelled orders"
            )

        total = self.db_session.scalar(
            select(func.sum(Job.price))
            .where(Job.order_id == order_id)
        ) or Decimal("0.00")

        paid = self.db_session.scalar(
            select(func.sum(Payment.amount))
            .where(Payment.order_id == order_id)
        ) or Decimal("0.00")

        remaining_total = total - job.price

        if remaining_total < paid:
            raise JobDeletionError(
                "Cannot delete this job because the remaining "
                "order total would be less than the amount already paid"
            )

        job_count = self.db_session.scalar(
            select(func.count(Job.id))
            .where(Job.order_id == order_id)
        )

        if job_count <= 1:
            raise JobDeletionError(
                "Cannot delete the last job from an order"
            )

        self.db_session.delete(job)
        self.db_session.commit()

        return True

    