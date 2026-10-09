from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    create_access_token,
)
from app.models.admin_user import AdminUser


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def authenticate_admin(
        self,
        email: str,
        password: str,
    ) -> str:

        normalized_email = email.strip().lower()

        admin = self.db_session.scalar(
            select(AdminUser).where(
                func.lower(AdminUser.email) == normalized_email
            )
        )

        if admin is None:
            raise InvalidCredentialsError(
                "Invalid email or password"
            )

        if not verify_password(
            password,
            admin.password_hash,
        ):
            raise InvalidCredentialsError(
                "Invalid email or password"
            )

        if not admin.is_active:
            raise InvalidCredentialsError(
                "Invalid email or password"
            )

        return create_access_token(admin.id)