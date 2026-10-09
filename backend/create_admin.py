from getpass import getpass

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.admin_user import AdminUser


def create_admin():
    email = input("Admin email: ").strip().lower()
    password = getpass("Admin password: ")
    confirm_password = getpass("Confirm password: ")

    if not email or "@" not in email:
        print("Please enter a valid email address.")
        return

    if len(password) < 12:
        print("Password must contain at least 12 characters.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    with SessionLocal() as db:
        existing_admin = db.scalar(
            select(AdminUser).where(
                func.lower(AdminUser.email) == email
            )
        )

        if existing_admin is not None:
            print("An administrator with this email already exists.")
            return

        admin = AdminUser(
            email=email,
            password_hash=hash_password(password),
            is_active=True,
        )

        db.add(admin)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            print("Could not create administrator. Check for duplicate data.")
            return

        print("Administrator created successfully!")


if __name__ == "__main__":
    create_admin()