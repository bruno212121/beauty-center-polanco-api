from sqlalchemy.orm import Session

from app.models.stylist_profile import StylistProfile
from app.schemas.stylist_profile import StylistProfileCreate, StylistProfileUpdate


def get_stylist_profile(db: Session, profile_id: int) -> StylistProfile | None:
    return db.get(StylistProfile, profile_id)


def get_stylist_profile_by_user(db: Session, user_id: int) -> StylistProfile | None:
    return (
        db.query(StylistProfile).filter(StylistProfile.user_id == user_id).first()
    )


def get_stylist_profiles(
    db: Session, active_only: bool = False, skip: int = 0, limit: int = 100
) -> list[StylistProfile]:
    q = db.query(StylistProfile)
    if active_only:
        q = q.filter(StylistProfile.active.is_(True))
    return q.offset(skip).limit(limit).all()


def create_stylist_profile(
    db: Session, data: StylistProfileCreate
) -> StylistProfile:
    profile = StylistProfile(**data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_stylist_profile(
    db: Session, profile: StylistProfile, data: StylistProfileUpdate
) -> StylistProfile:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile
