from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint

from app.database import Base
from sqlalchemy import Enum as SQLEnum
from app.models.enums import JobType

if TYPE_CHECKING:
    from app.models.order import Order

class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (
    CheckConstraint("price >= 0", name="ck_jobs_price_nonnegative"),
)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False)

    job_type: Mapped[JobType] = mapped_column(
    SQLEnum(JobType, name="job_type"),
    nullable=False)

    garment_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False)

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False)

    details: Mapped[str] = mapped_column(
        Text,
        nullable=False)

    order: Mapped["Order"] = relationship(
    back_populates="jobs")