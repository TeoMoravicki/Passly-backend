import secrets
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..guards.redis_client import get_redis
from .usuarios_model import AsignacionRol, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ROLES_VALIDOS = ("usuario", "administrador")
PASSWORD_RESET_TTL_SECONDS = 15 * 60


class UserService:
    def create_user(
        self, db: Session, name: str, email: str, password: str, birth_date: str
    ) -> User:
        usuario = User(
            name=name,
            email=email,
            password_hash=pwd_context.hash(password),
            birth_date=birth_date,
            role="usuario",
        )
        db.add(usuario)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una cuenta registrada con ese email",
            )
        db.refresh(usuario)
        return self.get_user(db, usuario.id)

    def get_user(self, db: Session, user_id: int) -> User:
        usuario = db.get(User, user_id)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario.role = self.obtener_rol_actual(db, user_id)
        db.expunge(usuario)
        return usuario

    def list_users(self, db: Session) -> list[User]:
        usuarios = db.scalars(select(User)).all()
        for usuario in usuarios:
            usuario.role = self.obtener_rol_actual(db, usuario.id)
        db.expunge_all()
        return list(usuarios)

    def authenticate(self, db: Session, email: str, password: str) -> User:
        credenciales_invalidas = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )

        usuario = db.scalar(select(User).where(User.email == email))
        if usuario is None or not pwd_context.verify(password, usuario.password_hash):
            raise credenciales_invalidas

        return self.get_user(db, usuario.id)

    def obtener_rol_actual(self, db: Session, user_id: int) -> str:
        ultima_asignacion = db.scalar(
            select(AsignacionRol)
            .where(AsignacionRol.user_id == user_id)
            .order_by(AsignacionRol.id.desc())
            .limit(1)
        )
        if ultima_asignacion is not None:
            return ultima_asignacion.rol

        usuario = db.get(User, user_id)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario.role

    def asignar_rol(self, db: Session, user_id: int, nuevo_rol: str) -> User:
        if nuevo_rol not in ROLES_VALIDOS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Rol invalido: tiene que ser uno de {ROLES_VALIDOS}",
            )
        if db.get(User, user_id) is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.add(AsignacionRol(user_id=user_id, rol=nuevo_rol))
        db.commit()

        return self.get_user(db, user_id)

    def solicitar_reset_password(self, db: Session, email: str) -> str | None:
        usuario = db.scalar(select(User).where(User.email == email))
        if usuario is None:
            return None
        
        token = secrets.token_urlsafe(32)
        get_redis().setex(
            f"pwd_reset:{token}", PASSWORD_RESET_TTL_SECONDS, str(usuario.id)
        )
        return token

    def resetear_password(self, db: Session, token: str, nueva_password: str) -> None:

        user_id = get_redis().getdel(f"pwd_reset:{token}")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El token de recuperacion es invalido o ya expiro",
            )

        usuario = db.get(User, int(user_id))
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario.password_hash = pwd_context.hash(nueva_password)
        db.commit()