from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProductSale(Base):
    __tablename__ = "product_sales"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    stylist_id: Mapped[int | None] = mapped_column(
        ForeignKey("stylist_profiles.id"), index=True
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    client: Mapped["Client"] = relationship("Client", back_populates="product_sales")  # noqa: F821
    stylist: Mapped["StylistProfile"] = relationship(  # noqa: F821
        "StylistProfile", back_populates="product_sales"
    )
    items: Mapped[list["ProductSaleItem"]] = relationship(
        "ProductSaleItem", back_populates="sale", cascade="all, delete-orphan"
    )


class ProductSaleItem(Base):
    __tablename__ = "product_sale_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("product_sales.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    sale: Mapped["ProductSale"] = relationship("ProductSale", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="sale_items")  # noqa: F821
