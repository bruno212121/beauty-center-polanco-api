from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.product import ProductOut


class ProductSaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class ProductSaleItemOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    product: ProductOut


class ProductSaleCreate(BaseModel):
    client_id: int
    stylist_id: int | None = None
    items: list[ProductSaleItemCreate]


class ProductSaleOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    client_id: int
    stylist_id: int | None
    total_amount: Decimal
    created_at: datetime
    items: list[ProductSaleItemOut]
