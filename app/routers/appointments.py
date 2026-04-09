from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin_or_receptionist
from app.crud import appointment as crud
from app.database import get_db
from app.models.appointment import AppointmentStatus
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentDetailOut,
    AppointmentUpdate,
)

router = APIRouter(prefix="/appointments", tags=["Citas"])


@router.get(
    "/",
    response_model=list[AppointmentDetailOut],
    dependencies=[Depends(require_admin_or_receptionist)],
)
def list_appointments(
    client_id: int | None = None,
    stylist_id: int | None = None,
    appointment_status: AppointmentStatus | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_appointments(
        db,
        client_id=client_id,
        stylist_id=stylist_id,
        status=appointment_status,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/",
    response_model=AppointmentDetailOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_or_receptionist)],
)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, data)


@router.get(
    "/{appointment_id}",
    response_model=AppointmentDetailOut,
    dependencies=[Depends(require_admin_or_receptionist)],
)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return appointment


@router.patch(
    "/{appointment_id}",
    response_model=AppointmentDetailOut,
    dependencies=[Depends(require_admin_or_receptionist)],
)
def update_appointment(
    appointment_id: int, data: AppointmentUpdate, db: Session = Depends(get_db)
):
    appointment = crud.get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    if appointment.status == AppointmentStatus.cancelled:
        raise HTTPException(
            status_code=400, detail="No se puede modificar una cita cancelada"
        )
    return crud.update_appointment(db, appointment, data)
