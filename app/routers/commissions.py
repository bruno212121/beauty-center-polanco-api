from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.crud import commission as crud
from app.database import get_db
from app.models.commission import CommissionSourceType
from app.models.user import User, UserRole
from app.schemas.commission import CommissionOut, CommissionSummary

router = APIRouter(prefix="/commissions", tags=["Comisiones"])


@router.get(
    "/stylist/{stylist_id}",
    response_model=list[CommissionOut],
)
def list_stylist_commissions(
    stylist_id: int,
    source_type: CommissionSourceType | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Un estilista solo puede ver sus propias comisiones;
    # admin puede ver cualquiera
    if current_user.role != UserRole.admin:
        if not current_user.stylist_profile or current_user.stylist_profile.id != stylist_id:
            raise HTTPException(status_code=403, detail="Acceso denegado")

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
