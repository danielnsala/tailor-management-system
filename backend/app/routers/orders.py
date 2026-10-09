from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.order import OrderCreate, OrderFinancialSummary, OrderResponse, OrderUpdate
from app.services.order_service import OrderDeletionError, OrderService
from app.services.payment_service import PaymentService
from app.core.dependencies import get_current_admin


router = APIRouter(
    prefix="/customers/{customer_id}/orders",
    tags=["Orders"],
    dependencies=[Depends(get_current_admin)],
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

@router.patch(
    "/{order_id}",
    response_model=OrderResponse,
)
def update_order_status(
    customer_id: int,
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
):
    service = OrderService(db)

    updated_order = service.update_order_status(
        customer_id,
        order_id,
        order_update.status,
    )

    if updated_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return updated_order

@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(
    customer_id: int,
    order_id: int,
    db: Session = Depends(get_db),
):
    service = OrderService(db)

    try:
        deleted = service.delete_order(
            customer_id,
            order_id,
        )

    except OrderDeletionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )