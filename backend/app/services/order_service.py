from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.job import Job
from app.models.order import Order
from app.models.enums import OrderStatus
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_order(self, customer_id: int, order_create: OrderCreate) -> Order | None:
        customer = self.db_session.get(Customer, customer_id)
        if customer is None:
            return None

        order_data = order_create.model_dump(exclude={"jobs"})
        jobs_data = order_create.jobs

        new_order = Order(
            customer_id=customer_id, 
            order_date=date.today(),
            status=OrderStatus.RECEIVED,
            **order_data)
        self.db_session.add(new_order)
        self.db_session.flush()

        for job_data in jobs_data:
            job = Job(order_id=new_order.id, **job_data.model_dump())
            self.db_session.add(job)

        self.db_session.commit()
        self.db_session.refresh(new_order)
        return new_order

    def get_orders(self, customer_id: int) -> list[Order] | None:
        customer = self.db_session.get(Customer, customer_id)
        if customer is None:
            return None
        return self.db_session.execute(
            select(Order).where(Order.customer_id == customer_id)
        ).scalars().all()


    def get_order(self, customer_id: int, order_id: int) -> Order | None:
        customer = self.db_session.get(Customer, customer_id)
        if customer is None:
            return None
        return self.db_session.execute(
            select(Order).where(
                Order.id == order_id,
                Order.customer_id == customer_id,
            )
        ).scalar_one_or_none()