from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.measurement_set import MeasurementSet


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    first_name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False)
    
    last_name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False)
    
    phone: Mapped[str] = mapped_column(
        String(20), 
        nullable=False)
    
    email: Mapped[str] = mapped_column(
        String(200), 
        nullable=True)
    
    notes: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False)

    orders: Mapped[list["Order"]] = relationship(
    back_populates="customer")

    measurement_sets: Mapped[list["MeasurementSet"]] = relationship(
    back_populates="customer")
    