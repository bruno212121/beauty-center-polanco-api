from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import (
    appointments,
    auth,
    clients,
    commissions,
    products,
    sales,
    services,
    stylists,
    users,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Beauty Center Polanco API",
    description="API para gestión de citas, clientes, productos, ventas y comisiones de estilistas",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(stylists.router)
app.include_router(clients.router)
app.include_router(services.router)
app.include_router(products.router)
app.include_router(appointments.router)
app.include_router(sales.router)
app.include_router(commissions.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Beauty Center Polanco API", "docs": "/docs"}
