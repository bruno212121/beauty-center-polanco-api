from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.crud import commission as crud
from app.database import get_db
from app.models.commission import CommissionSourceType
from app.schemas.commission import CommissionOut, CommissionSummary

router = APIRouter(prefix="/commissions", tags=["Comisiones"])


@router.get(
    "/stylist/{stylist_id}",
    response_model=list[CommissionOut],
    dependencies=[Depends(require_admin)],
)
def list_stylist_commissions(
    stylist_id: int,
    source_type: CommissionSourceType | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):

    return crud.get_commissions_by_stylist(
        db, stylist_id=stylist_id, source_type=source_type, skip=skip, limit=limit
    )


@router.get(
    "/stylist/{stylist_id}/summary",
    response_model=CommissionSummary,
    dependencies=[Depends(require_admin)],
)
def get_stylist_commission_summary(
    stylist_id: int, db: Session = Depends(get_db)
):
    service_commissions = crud.get_commissions_by_stylist(
        db, stylist_id=stylist_id, source_type=CommissionSourceType.service, limit=10000
    )
    product_commissions = crud.get_commissions_by_stylist(
        db, stylist_id=stylist_id, source_type=CommissionSourceType.product, limit=10000
    )
    total_service = sum((c.amount for c in service_commissions), Decimal("0.00"))
    total_product = sum((c.amount for c in product_commissions), Decimal("0.00"))

    return CommissionSummary(
        stylist_id=stylist_id,
        total_service_commissions=total_service,
        total_product_commissions=total_product,
        total=total_service + total_product,
    )
