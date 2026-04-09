from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.crud.commission import create_commission
from app.models.commission import CommissionSourceType
from app.models.product import Product
from app.models.product_sale import ProductSale, ProductSaleItem
from app.schemas.product_sale import ProductSaleCreate


def get_product_sale(db: Session, sale_id: int) -> ProductSale | None:
    return (
        db.query(ProductSale)
        .options(
            joinedload(ProductSale.items).joinedload(ProductSaleItem.product)
        )
        .filter(ProductSale.id == sale_id)
        .first()
    )


def get_product_sales(
    db: Session,
    client_id: int | None = None,
    stylist_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ProductSale]:
    q = db.query(ProductSale).options(
        joinedload(ProductSale.items).joinedload(ProductSaleItem.product)
    )
    if client_id:
        q = q.filter(ProductSale.client_id == client_id)
    if stylist_id:
        q = q.filter(ProductSale.stylist_id == stylist_id)
    return q.order_by(ProductSale.created_at.desc()).offset(skip).limit(limit).all()


def create_product_sale(db: Session, data: ProductSaleCreate) -> ProductSale:
    if not data.items:
        raise HTTPException(status_code=400, detail="La venta debe tener al menos un ítem")

    sale = ProductSale(
        client_id=data.client_id,
        stylist_id=data.stylist_id,
        total_amount=Decimal("0.00"),
    )
    db.add(sale)
    db.flush()  # obtener sale.id sin commit

    total = Decimal("0.00")

    for item_data in data.items:
        product = db.get(Product, item_data.product_id)
        if not product or not product.active:
            raise HTTPException(
                status_code=404,
                detail=f"Producto {item_data.product_id} no encontrado o inactivo",
            )
        if product.stock < item_data.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{product.name}' (disponible: {product.stock})",
            )

        unit_price = product.price
        subtotal = unit_price * item_data.quantity

        sale_item = ProductSaleItem(
            sale_id=sale.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )
        db.add(sale_item)

        product.stock -= item_data.quantity
        total += subtotal

    sale.total_amount = total
    db.commit()
    db.refresh(sale)

    # Generar comisión por venta si hay estilista asignado
    if data.stylist_id:
        create_commission(
            db=db,
            stylist_id=data.stylist_id,
            source_type=CommissionSourceType.product,
            source_id=sale.id,
            percentage=settings.COMMISSION_PRODUCT_PERCENT,
            base_amount=total,
        )

    return get_product_sale(db, sale.id)
