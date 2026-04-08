from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


def get_client(db: Session, client_id: int) -> Client | None:
    return db.get(Client, client_id)


def get_clients(
    db: Session, search: str | None = None, skip: int = 0, limit: int = 100
) -> list[Client]:
    q = db.query(Client)
    if search:
        q = q.filter(Client.full_name.ilike(f"%{search}%"))
    return q.order_by(Client.full_name).offset(skip).limit(limit).all()


def create_client(db: Session, data: ClientCreate) -> Client:
    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def update_client(db: Session, client: Client, data: ClientUpdate) -> Client:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client
