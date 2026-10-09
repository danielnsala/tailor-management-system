from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.order import JobUpdate, JobResponse
from app.services.job_service import JobService, InvalidJobPriceError
from app.core.dependencies import get_current_admin


router = APIRouter(
    prefix="/orders/{order_id}/jobs",
    tags=["Jobs"],
    dependencies=[Depends(get_current_admin)],
)

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