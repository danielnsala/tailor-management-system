from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy import Enum as SQLEnum
from app.models.enums import OrderStatus

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.job import Job
    from app.models.payment import Payment

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False)

    order_date: Mapped[date] = mapped_column(
        Date,
        nullable=False)

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False)

    status: Mapped[OrderStatus] = mapped_column(
    SQLEnum(OrderStatus, name="order_status"),
    nullable=False,
    default=OrderStatus.RECEIVED)

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)

    customer: Mapped["Customer"] = relationship(
    back_populates="orders")

    jobs: Mapped[list["Job"]] = relationship(
    back_populates="order")

    payments: Mapped[list["Payment"]] = relationship(
    back_populates="order")