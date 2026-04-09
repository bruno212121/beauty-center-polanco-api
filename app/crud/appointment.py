from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload

from app.crud.commission import create_commission
from app.models.appointment import Appointment, AppointmentStatus
from app.models.commission import CommissionSourceType
from app.models.service import Service
from app.models.stylist_profile import StylistProfile
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate

VALID_TRANSITIONS: dict[AppointmentStatus, list[AppointmentStatus]] = {
    AppointmentStatus.scheduled:   [AppointmentStatus.in_progress, AppointmentStatus.cancelled],
    AppointmentStatus.in_progress: [AppointmentStatus.completed, AppointmentStatus.cancelled],
    AppointmentStatus.completed:   [],
    AppointmentStatus.cancelled:   [],
}


def _check_stylist_availability(
    db: Session,
    stylist_id: int,
    start_time,
    end_time,
    exclude_appointment_id: int | None = None,
) -> None:
    """Lanza HTTPException si el estilista ya tiene una cita que se superpone."""
    q = db.query(Appointment).filter(
        Appointment.stylist_id == stylist_id,
        Appointment.status != AppointmentStatus.cancelled,
        or_(
            and_(
                Appointment.start_time < end_time,
                Appointment.end_time > start_time,
            )
        ),
    )
    if exclude_appointment_id:
        q = q.filter(Appointment.id != exclude_appointment_id)

    if q.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El estilista ya tiene una cita en ese horario",
        )


def get_appointment(db: Session, appointment_id: int) -> Appointment | None:
    return (
        db.query(Appointment)
        .options(
            joinedload(Appointment.client),
            joinedload(Appointment.stylist),
            joinedload(Appointment.service),
        )
        .filter(Appointment.id == appointment_id)
        .first()
    )


def get_appointments(
    db: Session,
    client_id: int | None = None,
    stylist_id: int | None = None,
    status: AppointmentStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Appointment]:
    q = db.query(Appointment).options(
        joinedload(Appointment.client),
        joinedload(Appointment.stylist),
        joinedload(Appointment.service),
    )
    if client_id:
        q = q.filter(Appointment.client_id == client_id)
    if stylist_id:
        q = q.filter(Appointment.stylist_id == stylist_id)
    if status:
        q = q.filter(Appointment.status == status)
    return q.order_by(Appointment.start_time.desc()).offset(skip).limit(limit).all()


def create_appointment(db: Session, data: AppointmentCreate) -> Appointment:
    service = db.get(Service, data.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    stylist = db.get(StylistProfile, data.stylist_id)
    if not stylist or not stylist.active:
        raise HTTPException(
            status_code=404, detail="Estilista no encontrado o inactivo"
        )

    end_time = data.start_time + timedelta(minutes=service.duration_minutes)

    _check_stylist_availability(db, data.stylist_id, data.start_time, end_time)

    appointment = Appointment(
        client_id=data.client_id,
        stylist_id=data.stylist_id,
        service_id=data.service_id,
        start_time=data.start_time,
        end_time=end_time,
        total_amount=service.price,
        notes=data.notes,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def update_appointment(
    db: Session, appointment: Appointment, data: AppointmentUpdate
) -> Appointment:
    updates = data.model_dump(exclude_unset=True)

    if "status" in updates:
        new_status = updates["status"]
        allowed = VALID_TRANSITIONS[appointment.status]
        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede cambiar el estado de '{appointment.status.value}' a '{new_status.value}'",
            )

    if "start_time" in updates:
        service = db.get(Service, appointment.service_id)
        new_end = updates["start_time"] + timedelta(minutes=service.duration_minutes)
        _check_stylist_availability(
            db,
            appointment.stylist_id,
            updates["start_time"],
            new_end,
            exclude_appointment_id=appointment.id,
        )
        updates["end_time"] = new_end

    previous_status = appointment.status

    for field, value in updates.items():
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)

    # Generar comisión al completar una cita
    if (
        previous_status != AppointmentStatus.completed
        and appointment.status == AppointmentStatus.completed
        and appointment.total_amount
    ):
        stylist = db.get(StylistProfile, appointment.stylist_id)
        if stylist and stylist.commission_service_percent > 0:
            create_commission(
                db=db,
                stylist_id=appointment.stylist_id,
                source_type=CommissionSourceType.service,
                source_id=appointment.id,
                percentage=stylist.commission_service_percent,
                base_amount=appointment.total_amount,
            )

    return appointment
