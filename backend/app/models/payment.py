from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint

from app.database import Base
from sqlalchemy import Enum as SQLEnum
from app.models.enums import PaymentMethod

if TYPE_CHECKING:
    from app.models.order import Order

class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
    CheckConstraint("amount > 0", name="ck_payments_amount_positive"),
)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False)

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False)

    payment_method: Mapped[PaymentMethod] = mapped_column(
    SQLEnum(PaymentMethod, name="payment_method"),
    nullable=False)

    payment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False)

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True)

    order: Mapped["Order"] = relationship(
    back_populates="payments")