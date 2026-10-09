from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import AdminLogin, TokenResponse
from app.services.auth_service import (
    AuthService,
    InvalidCredentialsError,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    credentials: AdminLogin,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        access_token = service.authenticate_admin(
            credentials.email,
            credentials.password,
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return TokenResponse(
        access_token=access_token,
    )