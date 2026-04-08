from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin_or_receptionist
from app.crud import product_sale as crud
from app.database import get_db
from app.schemas.product_sale import ProductSaleCreate, ProductSaleOut

router = APIRouter(prefix="/sales", tags=["Ventas de productos"])


@router.get("/", response_model=list[ProductSaleOut],
            dependencies=[Depends(get_current_user)])
def list_sales(
    client_id: int | None = None,
    stylist_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_product_sales(
        db, client_id=client_id, stylist_id=stylist_id, skip=skip, limit=limit
    )


@router.post(
    "/",
    response_model=ProductSaleOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_or_receptionist)],
)
def create_sale(data: ProductSaleCreate, db: Session = Depends(get_db)):
    return crud.create_product_sale(db, data)


@router.get("/{sale_id}", response_model=ProductSaleOut,
            dependencies=[Depends(get_current_user)])
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = crud.get_product_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return sale
