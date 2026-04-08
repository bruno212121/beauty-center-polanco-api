import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CommissionSourceType(str, enum.Enum):
    service = "service"
    product = "product"


class Commission(Base):
    __tablename__ = "commissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey("stylist_profiles.id"), index=True
    )
    source_type: Mapped[CommissionSourceType] = mapped_column(
        Enum(CommissionSourceType)
    )
    source_id: Mapped[int] = mapped_column(Integer)
    percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    stylist: Mapped["StylistProfile"] = relationship(  # noqa: F821
        "StylistProfile", back_populates="commissions"
    )
