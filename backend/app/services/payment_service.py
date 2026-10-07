from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.order import Order
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate


class OverpaymentError(Exception):
    pass


class PaymentService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_payment(
        self,
        order_id: int,
        payment_create: PaymentCreate,
    ) -> Payment | None:
        order = self.db_session.get(Order, order_id)
        if order is None:
            return None

        balance_info = self.get_order_balance(order_id)
        if balance_info is None:
            return None
        total, paid, balance = balance_info

        if payment_create.amount > balance:
            raise OverpaymentError(f"Payment exceeds remaining balance of ${balance:.2f}")

        payment = Payment(order_id=order_id, **payment_create.model_dump())
        self.db_session.add(payment)
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment

    def get_payments(
        self,
        order_id: int,
    ) -> list[Payment] | None:
        order = self.db_session.get(Order, order_id)

        if order is None:
            return None

        return self.db_session.execute(
            select(Payment).where(
                Payment.order_id == order_id
            )
        ).scalars().all()

    def get_order_balance(
        self,
        order_id: int,
    ) -> tuple[Decimal, Decimal, Decimal] | None:
        order = self.db_session.get(Order, order_id)

        if order is None:
            return None

        total = self.db_session.scalar(
            select(func.sum(Job.price)).where(
                Job.order_id == order_id
            )
        ) or Decimal("0.00")

        paid = self.db_session.scalar(
            select(func.sum(Payment.amount)).where(
                Payment.order_id == order_id
            )
        ) or Decimal("0.00")

        balance = total - paid

        return total, paid, balance

    