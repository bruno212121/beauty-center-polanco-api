from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.commission import Commission, CommissionSourceType


def create_commission(
    db: Session,
    stylist_id: int,
    source_type: CommissionSourceType,
    source_id: int,
    percentage: Decimal,
    base_amount: Decimal,
) -> Commission:
    amount = (base_amount * percentage / Decimal("100")).quantize(Decimal("0.01"))
    commission = Commission(
        stylist_id=stylist_id,
        source_type=source_type,
        source_id=source_id,
        percentage=percentage,
        amount=amount,
    )
    db.add(commission)
    db.commit()
    db.refresh(commission)
    return commission


def get_commissions_by_stylist(
    db: Session,
    stylist_id: int,
    source_type: CommissionSourceType | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Commission]:
    q = db.query(Commission).filter(Commission.stylist_id == stylist_id)
    if source_type:
        q = q.filter(Commission.source_type == source_type)
    if date_from:
        q = q.filter(Commission.created_at >= date_from)
    if date_to:
        q = q.filter(Commission.created_at <= date_to)
    return q.order_by(Commission.created_at.desc()).offset(skip).limit(limit).all()
