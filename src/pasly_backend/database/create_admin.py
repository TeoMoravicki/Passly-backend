from pasly_backend.database.database import SessionLocal
from pasly_backend.usuarios.usuarios_model import User
from pasly_backend.usuarios.usuarios_service import pwd_context


ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "123"


def create_admin_user() -> None:
    db = SessionLocal()
    try:
        ya_existe = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if ya_existe is not None:
            return

        admin = User(
            name="admin",
            email=ADMIN_EMAIL,
            password_hash=pwd_context.hash(ADMIN_PASSWORD),
            birth_date="01-01-2004",
            role="administrador",
        )
        db.add(admin)
        db.commit()
    finally:
        db.close()