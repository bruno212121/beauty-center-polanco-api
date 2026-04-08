from sqlalchemy.orm import Session

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


def get_service(db: Session, service_id: int) -> Service | None:
    return db.get(Service, service_id)


def get_services(
    db: Session,
    active_only: bool = False,
    category: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Service]:
    q = db.query(Service)
    if active_only:
        q = q.filter(Service.active.is_(True))
    if category:
        q = q.filter(Service.category == category)
    return q.order_by(Service.name).offset(skip).limit(limit).all()


def create_service(db: Session, data: ServiceCreate) -> Service:
    service = Service(**data.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def update_service(db: Session, service: Service, data: ServiceUpdate) -> Service:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service
