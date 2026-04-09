from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StylistProfile(Base):
    __tablename__ = "stylist_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    specialty: Mapped[str | None] = mapped_column(String(150))
 
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User", back_populates="stylist_profile")  # noqa: F821
    appointments: Mapped[list["Appointment"]] = relationship(  # noqa: F821
        "Appointment", back_populates="stylist"
    )
    product_sales: Mapped[list["ProductSale"]] = relationship(  # noqa: F821
        "ProductSale", back_populates="stylist"
    )
    commissions: Mapped[list["Commission"]] = relationship(  # noqa: F821
        "Commission", back_populates="stylist"
    )
