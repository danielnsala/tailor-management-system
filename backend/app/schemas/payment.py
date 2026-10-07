from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import PaymentMethod


PositiveMoney = Annotated[
    Decimal,
    Field(gt=0, max_digits=10, decimal_places=2),
]


class PaymentCreate(BaseModel):
    amount: PositiveMoney
    payment_method: PaymentMethod
    payment_date: date
    notes: str | None = None


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    amount: Decimal
    payment_method: PaymentMethod
    payment_date: date
    notes: str | None = None