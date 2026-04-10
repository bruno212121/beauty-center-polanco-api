from pydantic import BaseModel

from app.schemas.client import ClientOut
from app.schemas.appointment import AppointmentOut
from app.schemas.product_sale import ProductSaleOut


class ClientHistoryOut(ClientOut):
    appointments: list[AppointmentOut]
    product_sales: list[ProductSaleOut]
