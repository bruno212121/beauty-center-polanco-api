from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.receptionist


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str


class UserOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    full_name: str
    email: str
    role: UserRole
