from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService, OverpaymentError
from app.core.dependencies import get_current_admin

router = APIRouter(
    prefix="/orders/{order_id}/payments",
    tags=["Payments"],
    dependencies=[Depends(get_current_admin)],
)

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    order_id: int,
    payment_create: PaymentCreate,
    db: Session = Depends(get_db),
):
    service = PaymentService(db)
    try:
        new_payment = service.create_payment(order_id, payment_create)
    except OverpaymentError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    if new_payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return new_payment

@router.get("/", response_model=list[PaymentResponse])
def get_payments(
    order_id: int,
    db: Session = Depends(get_db),
):
    service = PaymentService(db)
    payments = service.get_payments(order_id)
    if payments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return payments