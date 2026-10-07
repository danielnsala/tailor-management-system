from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, UniqueConstraint

from app.database import Base

if TYPE_CHECKING:
    from app.models.measurement_set import MeasurementSet

class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = (
    CheckConstraint(
        "value > 0",
        name="ck_measurements_value_positive",
    ),
    UniqueConstraint(
        "measurement_set_id",
        "measurement_type",
        name="uq_measurement_set_type",
    ),
)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    measurement_set_id: Mapped[int] = mapped_column(
        ForeignKey("measurement_sets.id"),
        nullable=False)

    measurement_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False)

    value: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False)

    measurement_set: Mapped["MeasurementSet"] = relationship(
    back_populates="measurements")