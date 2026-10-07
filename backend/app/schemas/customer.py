from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr | None = None
    notes: str | None = None

class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    notes: str | None = None

class CustomerResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True)

    id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr | None = None
    notes: str | None = None
    created_at: datetime