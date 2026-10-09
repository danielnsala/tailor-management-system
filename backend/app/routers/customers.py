from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)
from app.services.customer_service import CustomerService

from app.core.dependencies import get_current_admin

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(get_current_admin)],
)

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_create: CustomerCreate,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)
    new_customer = service.create_customer(customer_create)
    return new_customer

@router.get("/", response_model=list[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    service = CustomerService(db)
    customers = service.get_all_customers()
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)
    updated_customer = service.update_customer(customer_id, customer_update)
    if not updated_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return updated_customer

@router.patch("/{customer_id}", response_model=CustomerResponse)
def partial_update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)
    updated_customer = service.update_customer(customer_id, customer_update)
    if not updated_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return updated_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    success = service.delete_customer(customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return None
