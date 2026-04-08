from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin_or_receptionist
from app.crud import client as crud
from app.database import get_db
from app.models.user import User
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate

router = APIRouter(prefix="/clients", tags=["Clientes"])


@router.get(
    "/",
    response_model=list[ClientOut],
    dependencies=[Depends(get_current_user)],
)
def list_clients(
    search: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_clients(db, search=search, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=ClientOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_or_receptionist)],
)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, data)


@router.get(
    "/{client_id}",
    response_model=ClientOut,
    dependencies=[Depends(get_current_user)],
)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client


@router.patch(
    "/{client_id}",
    response_model=ClientOut,
    dependencies=[Depends(require_admin_or_receptionist)],
)
def update_client(client_id: int, data: ClientUpdate, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return crud.update_client(db, client, data)
