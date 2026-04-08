from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.user import UserOut


class StylistProfileCreate(BaseModel):
    user_id: int
    specialty: str | None = None
    commission_service_percent: Decimal = Field(default=Decimal("0.00"), ge=0, le=100)
    commission_product_percent: Decimal = Field(default=Decimal("0.00"), ge=0, le=100)
    active: bool = True


class StylistProfileUpdate(BaseModel):
    specialty: str | None = None
    commission_service_percent: Decimal | None = Field(default=None, ge=0, le=100)
    commission_product_percent: Decimal | None = Field(default=None, ge=0, le=100)
    active: bool | None = None


class StylistProfileOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    user_id: int
    specialty: str | None
    commission_service_percent: Decimal
    commission_product_percent: Decimal
    active: bool


class StylistProfileWithUserOut(StylistProfileOut):
    user: UserOut
