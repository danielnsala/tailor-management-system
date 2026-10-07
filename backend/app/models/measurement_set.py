from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy import Enum as SQLEnum
from app.models.enums import MeasurementUnit

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.measurement import Measurement

class MeasurementSet(Base):
    __tablename__ = "measurement_sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False)

    date_taken: Mapped[date] = mapped_column(
        Date,
        nullable=False)

    unit: Mapped[MeasurementUnit] = mapped_column(
    SQLEnum(MeasurementUnit, name="measurement_unit"),
    nullable=False)

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True)

    customer: Mapped["Customer"] = relationship(
    back_populates="measurement_sets")

    measurements: Mapped[list["Measurement"]] = relationship(
    back_populates="measurement_set")