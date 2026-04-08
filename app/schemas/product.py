from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    brand: str | None = None
    category: str | None = None
    price: Decimal = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    min_stock: int = Field(default=0, ge=0)
    active: bool = True


class ProductUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    category: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    min_stock: int | None = Field(default=None, ge=0)
    active: bool | None = None


class ProductOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    brand: str | None
    category: str | None
    price: Decimal
    stock: int
    min_stock: int
    active: bool
    low_stock: bool = False

    @classmethod
    def model_validate(cls, obj, **kwargs):
        instance = super().model_validate(obj, **kwargs)
        instance.low_stock = obj.stock <= obj.min_stock
        return instance
