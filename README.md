# Beauty Center Polanco — API

Backend REST construido con **FastAPI** y **SQLAlchemy** para gestionar citas, clientes, productos, ventas y comisiones de estilistas.

---

## Stack

| Tecnología | Uso |
|---|---|
| FastAPI | Framework HTTP |
| SQLAlchemy 2.x | ORM / modelos |
| Alembic | Migraciones de base de datos |
| PostgreSQL | Base de datos |
| Pydantic v2 | Validación y serialización |
| passlib + bcrypt | Hash de contraseñas |
| python-jose | JWT |

---

## Estructura del proyecto

```
app/
├── main.py              # Entrada de la aplicación
├── config.py            # Variables de entorno
├── database.py          # Conexión y sesión de BD
├── models/              # Modelos SQLAlchemy
├── schemas/             # Schemas Pydantic (request/response)
├── crud/                # Lógica de acceso a datos y negocio
├── routers/             # Endpoints agrupados por recurso
└── core/
    ├── security.py      # Hash, JWT
    └── dependencies.py  # Dependencias de FastAPI (auth, roles)
```

---

## Instalación

```bash
# 1. Clonar el repo y entrar
git clone <repo-url>
cd beauty-center-polanco-api

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

---

## Ejecutar

```bash
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/auth/login` | Iniciar sesión (JWT) |
| GET | `/auth/me` | Usuario autenticado |
| GET/POST | `/users/` | Gestión de usuarios |
| GET/POST | `/stylists/` | Perfiles de estilistas |
| GET/POST | `/clients/` | Clientes del salón |
| GET/POST | `/services/` | Catálogo de servicios |
| GET/POST | `/products/` | Catálogo e inventario |
| GET/POST | `/appointments/` | Agenda de citas |
| GET/POST | `/sales/` | Ventas de productos |
| GET | `/commissions/stylist/{id}` | Comisiones por estilista |
| GET | `/commissions/stylist/{id}/summary` | Resumen de comisiones |

---

## Roles

| Rol | Permisos |
|---|---|
| `admin` | Acceso total |
| `receptionist` | Gestión de citas, clientes, ventas |
| `stylist` | Lectura de sus propios datos |

---

## Lógica de negocio relevante

- Al crear una cita, `end_time` se calcula automáticamente con `service.duration_minutes`.
- Se valida que el estilista no tenga superposición de horarios.
- Al marcar una cita como `completed`, se genera automáticamente una `Commission` de tipo `service`.
- Al registrar una venta, el stock de cada producto se reduce y se genera una `Commission` de tipo `product` si el estilista tiene porcentaje configurado.
- El endpoint `GET /products/?low_stock_only=true` permite obtener alertas de inventario bajo.
