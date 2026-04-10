from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.crud import commission as crud
from app.database import get_db
from app.models.commission import CommissionSourceType
from app.schemas.commission import CommissionOut, CommissionSummary

router = APIRouter(prefix="/commissions", tags=["Comisiones"])


class ReportPeriod(str, Enum):
    weekly = "weekly"
    monthly = "monthly"


def _resolve_dates(
    period: ReportPeriod | None,
    date_from: datetime | None,
    date_to: datetime | None,
) -> tuple[datetime | None, datetime | None]:
    if period == ReportPeriod.weekly:
        now = datetime.now()
        return now - timedelta(days=7), now
    if period == ReportPeriod.monthly:
        now = datetime.now()
        return now - timedelta(days=30), now
    return date_from, date_to


@router.get(
    "/stylist/{stylist_id}",
    response_model=list[CommissionOut],
    dependencies=[Depends(require_admin)],
)
def list_stylist_commissions(
    stylist_id: int,
    source_type: CommissionSourceType | None = None,
    period: ReportPeriod | None = Query(None, description="Atajo: weekly o monthly"),
    date_from: datetime | None = Query(None, description="Fecha inicio (ISO 8601)"),
    date_to: datetime | None = Query(None, description="Fecha fin (ISO 8601)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    date_from, date_to = _resolve_dates(period, date_from, date_to)
    return crud.get_commissions_by_stylist(
        db,
        stylist_id=stylist_id,
        source_type=source_type,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/stylist/{stylist_id}/summary",
    response_model=CommissionSummary,
    dependencies=[Depends(require_admin)],
)
def get_stylist_commission_summary(
    stylist_id: int,
    period: ReportPeriod | None = Query(None, description="Atajo: weekly o monthly"),
    date_from: datetime | None = Query(None, description="Fecha inicio (ISO 8601)"),
    date_to: datetime | None = Query(None, description="Fecha fin (ISO 8601)"),
    db: Session = Depends(get_db),
):
    date_from, date_to = _resolve_dates(period, date_from, date_to)
    service_commissions = crud.get_commissions_by_stylist(
        db,
        stylist_id=stylist_id,
        source_type=CommissionSourceType.service,
        date_from=date_from,
        date_to=date_to,
        limit=10000,
    )
    product_commissions = crud.get_commissions_by_stylist(
        db,
        stylist_id=stylist_id,
        source_type=CommissionSourceType.product,
        date_from=date_from,
        date_to=date_to,
        limit=10000,
    )
    total_service = sum((c.amount for c in service_commissions), Decimal("0.00"))
    total_product = sum((c.amount for c in product_commissions), Decimal("0.00"))

    return CommissionSummary(
        stylist_id=stylist_id,
        total_service_commissions=total_service,
        total_product_commissions=total_product,
        total=total_service + total_product,
    )
