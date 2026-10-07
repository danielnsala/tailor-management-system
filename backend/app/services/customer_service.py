from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_customer(self, customer_create: CustomerCreate) -> Customer:
        new_customer = Customer(**customer_create.model_dump())
        self.db_session.add(new_customer)
        self.db_session.commit()
        self.db_session.refresh(new_customer)
        return new_customer

    def get_all_customers(self) -> list[Customer]:
        return self.db_session.execute(select(Customer)).scalars().all()

    def get_customer(self, customer_id: int) -> Customer | None:
        return self.db_session.get(Customer, customer_id)

    def update_customer(self, customer_id: int, customer_update: CustomerUpdate) -> Customer | None:
        customer = self.get_customer(customer_id)
        if not customer:
            return None
        for key, value in customer_update.model_dump(exclude_unset=True).items():
            setattr(customer, key, value)
        self.db_session.commit()
        self.db_session.refresh(customer)
        return customer

    def delete_customer(self, customer_id: int) -> bool:
        customer = self.get_customer(customer_id)
        if not customer:
            return False
        self.db_session.delete(customer)
        self.db_session.commit()
        return True