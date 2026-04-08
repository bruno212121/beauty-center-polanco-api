import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey("stylist_profiles.id"), index=True
    )
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus), default=AppointmentStatus.scheduled
    )
    total_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    client: Mapped["Client"] = relationship("Client", back_populates="appointments")  # noqa: F821
    stylist: Mapped["StylistProfile"] = relationship(  # noqa: F821
        "StylistProfile", back_populates="appointments"
    )
    service: Mapped["Service"] = relationship("Service", back_populates="appointments")  # noqa: F821
