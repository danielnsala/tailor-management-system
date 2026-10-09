from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.measurement import (
    MeasurementSetCreate,
    MeasurementSetResponse,
)
from app.services.measurement_service import MeasurementService
from app.core.dependencies import get_current_admin


router = APIRouter(
    prefix="/customers/{customer_id}/measurement-sets",
    tags=["Measurements"],
    dependencies=[Depends(get_current_admin)],
)

@router.post("/", response_model=MeasurementSetResponse, status_code=status.HTTP_201_CREATED)
def create_measurement_set(
    customer_id: int,
    measurement_set_create: MeasurementSetCreate,
    db: Session = Depends(get_db),
):
    service = MeasurementService(db)
    new_measurement_set = service.create_measurement_set(customer_id, measurement_set_create)
    if not new_measurement_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return new_measurement_set

@router.get("/", response_model=list[MeasurementSetResponse])
def get_measurement_sets(
    customer_id: int,
    db: Session = Depends(get_db),
):
    service = MeasurementService(db)
    measurement_sets = service.get_measurement_sets(customer_id)
    if measurement_sets is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return measurement_sets

@router.get("/{measurement_set_id}", response_model=MeasurementSetResponse)
def get_measurement_set(
    customer_id: int,
    measurement_set_id: int,
    db: Session = Depends(get_db),
):
    service = MeasurementService(db)
    measurement_set = service.get_measurement_set(customer_id, measurement_set_id)
    if not measurement_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement set not found",
        )
    return measurement_set