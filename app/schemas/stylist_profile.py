from pydantic import BaseModel, Field

from app.schemas.user import UserOut


class StylistProfileCreate(BaseModel):
    user_id: int
    specialty: str | None = None
    active: bool = True


class StylistProfileUpdate(BaseModel):
    specialty: str | None = None
    active: bool | None = None


class StylistProfileOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    user_id: int
    specialty: str | None
    active: bool


class StylistProfileWithUserOut(StylistProfileOut):
    user: UserOut
