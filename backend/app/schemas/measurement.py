from datetime import date
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import MeasurementUnit


PositiveDecimal = Annotated[
    Decimal,
    Field(gt=0)
]

class MeasurementCreate(BaseModel):
    measurement_type: str
    value: PositiveDecimal

class MeasurementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    measurement_type: str
    value: Decimal

class MeasurementSetCreate(BaseModel):
    date_taken: date
    unit: MeasurementUnit
    notes: str | None = None
    measurements: list[MeasurementCreate]

class MeasurementSetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    date_taken: date
    unit: MeasurementUnit
    notes: str | None = None
    measurements: list[MeasurementResponse]