from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin, require_admin_or_receptionist
from app.crud import stylist_profile as crud
from app.database import get_db
from app.schemas.stylist_profile import (
    StylistProfileCreate,
    StylistProfileUpdate,
    StylistProfileWithUserOut,
)

router = APIRouter(prefix="/stylists", tags=["Estilistas"])


@router.get(
    "/",
    response_model=list[StylistProfileWithUserOut],
    dependencies=[Depends(require_admin_or_receptionist)],
)
def list_stylists(
    active_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_stylist_profiles(db, active_only=active_only, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=StylistProfileWithUserOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_stylist(data: StylistProfileCreate, db: Session = Depends(get_db)):
    if crud.get_stylist_profile_by_user(db, data.user_id):
        raise HTTPException(
            status_code=400, detail="Ese usuario ya tiene un perfil de estilista"
        )
    return crud.create_stylist_profile(db, data)


@router.get(
    "/{profile_id}",
    response_model=StylistProfileWithUserOut,
    dependencies=[Depends(require_admin_or_receptionist)],
)
def get_stylist(profile_id: int, db: Session = Depends(get_db)):
    profile = crud.get_stylist_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil de estilista no encontrado")
    return profile


@router.patch(
    "/{profile_id}",
    response_model=StylistProfileWithUserOut,
    dependencies=[Depends(require_admin)],
)
def update_stylist(
    profile_id: int, data: StylistProfileUpdate, db: Session = Depends(get_db)
):
    profile = crud.get_stylist_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil de estilista no encontrado")
    return crud.update_stylist_profile(db, profile, data)
