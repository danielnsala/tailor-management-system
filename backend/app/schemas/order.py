from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import JobType, OrderStatus


Money = Annotated[
    Decimal,
    Field(ge=0, max_digits=10, decimal_places=2),
]

class JobCreate(BaseModel):
    job_type: JobType
    garment_type: str
    price: Money
    details: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_type: JobType
    garment_type: str
    price: Decimal
    details: str

class OrderCreate(BaseModel):
    due_date: date
    notes: str | None = None
    jobs: list[JobCreate] = Field(
        min_length=1, 
        description="List of jobs associated with the order. Must contain at least one job.")

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    order_date: date
    due_date: date
    status: OrderStatus
    notes: str | None = None
    created_at: datetime

    jobs: list[JobResponse]