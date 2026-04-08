from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def get_products(
    db: Session,
    active_only: bool = False,
    category: str | None = None,
    low_stock_only: bool = False,
    skip: int = 0,
    limit: int = 100,
) -> list[Product]:
    q = db.query(Product)
    if active_only:
        q = q.filter(Product.active.is_(True))
    if category:
        q = q.filter(Product.category == category)
    if low_stock_only:
        q = q.filter(Product.stock <= Product.min_stock)
    return q.order_by(Product.name).offset(skip).limit(limit).all()


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, data: ProductUpdate) -> Product:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def adjust_stock(db: Session, product: Product, delta: int) -> Product:
    """Delta positivo suma stock, negativo lo reduce."""
    product.stock += delta
    db.commit()
    db.refresh(product)
    return product
