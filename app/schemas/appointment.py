from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.appointment import AppointmentStatus
from app.schemas.client import ClientOut
from app.schemas.service import ServiceOut
from app.schemas.stylist_profile import StylistProfileOut


class AppointmentCreate(BaseModel):
    client_id: int
    stylist_id: int
    service_id: int
    start_time: datetime
    notes: str | None = None

    # end_time se calcula automáticamente en el CRUD a partir de la duración del servicio


class AppointmentUpdate(BaseModel):
    start_time: datetime | None = None
    notes: str | None = None
    status: AppointmentStatus | None = None


class AppointmentOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    client_id: int
    stylist_id: int
    service_id: int
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus
    total_amount: Decimal | None
    notes: str | None
    created_at: datetime


class AppointmentDetailOut(AppointmentOut):
    client: ClientOut
    stylist: StylistProfileOut
    service: ServiceOut
