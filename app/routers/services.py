from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin, require_admin_or_receptionist
from app.crud import service as crud
from app.database import get_db
from app.schemas.service import ServiceCreate, ServiceOut, ServiceUpdate

router = APIRouter(prefix="/services", tags=["Servicios"])


@router.get("/", response_model=list[ServiceOut], dependencies=[Depends(require_admin_or_receptionist)])
def list_services(
    active_only: bool = False,
    category: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_services(db, active_only=active_only, category=category,
                             skip=skip, limit=limit)


@router.post(
    "/",
    response_model=ServiceOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db, data)


@router.get("/{service_id}", response_model=ServiceOut,
            dependencies=[Depends(require_admin_or_receptionist)])
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = crud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return service


@router.patch("/{service_id}", response_model=ServiceOut,
              dependencies=[Depends(require_admin)])
def update_service(service_id: int, data: ServiceUpdate, db: Session = Depends(get_db)):
    service = crud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return crud.update_service(db, service, data)
