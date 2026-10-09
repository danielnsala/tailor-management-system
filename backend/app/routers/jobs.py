from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.order import JobCreate, JobUpdate, JobResponse
from app.services.job_service import JobDeletionError, JobService, InvalidJobPriceError, OrderNotEditableError
from app.core.dependencies import get_current_admin


router = APIRouter(
    prefix="/orders/{order_id}/jobs",
    tags=["Jobs"],
    dependencies=[Depends(get_current_admin)],
)

@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    order_id: int,
    job_create: JobCreate,
    db: Session = Depends(get_db),
):
    service = JobService(db)

    new_job = service.create_job(
        order_id,
        job_create,
    )

    if new_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return new_job

@router.get("/", response_model=list[JobResponse])
def get_jobs(
    order_id: int,
    db: Session = Depends(get_db),
):
    service = JobService(db)
    jobs = service.get_jobs(order_id)

    if jobs is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return jobs


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    order_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):
    service = JobService(db)
    job = service.get_job(order_id, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job

@router.patch(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    order_id: int,
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db),
):
    service = JobService(db)

    try:
        updated_job = service.update_job(
            order_id,
            job_id,
            job_update,
        )
    except InvalidJobPriceError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if updated_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found for this order",
        )

    return updated_job

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job(
    order_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):
    service = JobService(db)

    try:
        deleted = service.delete_job(order_id, job_id)

    except (JobDeletionError, OrderNotEditableError) as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order or job not found",
        )