from datetime import datetime

from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    full_name: str
    phone: str | None = None
    email: EmailStr | None = None
    preferences: str | None = None
    allergies: str | None = None
    notes: str | None = None


class ClientUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    preferences: str | None = None
    allergies: str | None = None
    notes: str | None = None


class ClientOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    full_name: str
    phone: str | None
    email: str | None
    preferences: str | None
    allergies: str | None
    notes: str | None
    created_at: datetime