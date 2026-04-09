
from app.database import SessionLocal, engine, Base
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate
from app.models.user import UserRole

Base.metadata.create_all(bind=engine)


def main():
    db = SessionLocal()
    try:
        email = input("Email del administrador: ").strip()
        if get_user_by_email(db, email):
            print(f"Ya existe un usuario con el email '{email}'.")
            return

        full_name = input("Nombre completo: ").strip()
        password = input("Contraseña: ").strip()

        user = create_user(
            db,
            UserCreate(
                full_name="Nombre del administrador",
                email="email@del.administrador",
                password="contraseña_del_administrador",
                role=UserRole.admin,
            ),
        )
        print(f"\nUsuario administrador creado exitosamente.")
        print(f"  ID:     {user.id}")
        print(f"  Nombre: {user.full_name}")
        print(f"  Email:  {user.email}")
        print(f"  Rol:    {user.role}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
