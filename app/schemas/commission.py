from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.commission import CommissionSourceType


class CommissionOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    stylist_id: int
    source_type: CommissionSourceType
    source_id: int
    percentage: Decimal
    amount: Decimal
    created_at: datetime


class CommissionSummary(BaseModel):
    stylist_id: int
    total_service_commissions: Decimal
    total_product_commissions: Decimal
    total: Decimal
