from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.measurement import Measurement
from app.models.measurement_set import MeasurementSet
from app.schemas.measurement import MeasurementSetCreate


class MeasurementService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_measurement_set(
        self,
        customer_id: int,
        measurement_set_create: MeasurementSetCreate,
    ) -> MeasurementSet | None:
        customer = self.db_session.get(Customer, customer_id)
        if customer is None:
            return None

        set_data = measurement_set_create.model_dump(exclude={"measurements"})
        measurements = measurement_set_create.measurements

        measurement_set = MeasurementSet(customer_id=customer_id, **set_data)
        self.db_session.add(measurement_set)
        self.db_session.flush()

        for measurement_data in measurements:
            measurement = Measurement(
                measurement_set_id=measurement_set.id,
                measurement_type=measurement_data.measurement_type,
                value=measurement_data.value,
            )
            self.db_session.add(measurement)

        self.db_session.commit()
        self.db_session.refresh(measurement_set)
        return measurement_set

    def get_measurement_sets(
        self,
        customer_id: int,
    ) -> list[MeasurementSet] | None:
        customer = self.db_session.get(Customer, customer_id)
        if customer is None:
            return None

        return self.db_session.execute(
            select(MeasurementSet).where(
                MeasurementSet.customer_id == customer_id
            )
        ).scalars().all()

    def get_measurement_set(
        self,
        customer_id: int,
        measurement_set_id: int,
    ) -> MeasurementSet | None:
        return self.db_session.execute(
            select(MeasurementSet).where(
                MeasurementSet.id == measurement_set_id,
                MeasurementSet.customer_id == customer_id,
            )
        ).scalar_one_or_none()