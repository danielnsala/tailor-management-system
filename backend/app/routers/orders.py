from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.order import OrderCreate, OrderFinancialSummary, OrderResponse
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService


router = APIRouter(
    prefix="/customers/{customer_id}/orders",
    tags=["Orders"],
)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    customer_id: int,
    order_create: OrderCreate,
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    new_order = service.create_order(customer_id, order_create)
    if not new_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return new_order

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    customer_id: int,
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    orders = service.get_orders(customer_id)
    if orders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    customer_id: int,
    order_id: int,
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    order = service.get_order(customer_id, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order

@router.get(
    "/{order_id}/financial-summary",
    response_model=OrderFinancialSummary,
)
def get_order_financial_summary(
    customer_id: int,
    order_id: int,
    db: Session = Depends(get_db),
):
    order_service = OrderService(db)

    order = order_service.get_order(customer_id, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found for this customer",
        )

    payment_service = PaymentService(db)
    balance_info = payment_service.get_order_balance(order_id)

    if balance_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    total, paid, balance = balance_info

    return OrderFinancialSummary(
        order_id=order_id,
        total_price=total,
        amount_paid=paid,
        balance=balance,
    )
