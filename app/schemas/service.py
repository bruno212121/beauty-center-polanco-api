from decimal import Decimal

from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    name: str
    category: str | None = None
    duration_minutes: int = Field(default=60, gt=0)
    price: Decimal = Field(gt=0)
    description: str | None = None
    active: bool = True


class ServiceUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    duration_minutes: int | None = Field(default=None, gt=0)
    price: Decimal | None = Field(default=None, gt=0)
    description: str | None = None
    active: bool | None = None


class ServiceOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    category: str | None
    duration_minutes: int
    price: Decimal
    description: str | None
    active: bool
