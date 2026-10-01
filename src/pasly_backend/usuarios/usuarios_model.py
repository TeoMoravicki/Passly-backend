from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pasly_backend.database.database import Base

def _timestamp() -> str:
    # formato 'YYYY-MM-DD HH:MM:SS'
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

class User(Base):
    __tablename__ = "usuarios"
    __table_args__ = (CheckConstraint("role IN ('usuario', 'administrador')", name="ck_usuarios_role"))
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[str] = mapped_column(String(10), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="usuario")
    created_at: Mapped[str] = mapped_column(String(19), nullable=False, default=_timestamp)

    asignaciones_rol: Mapped[list["AsignacionRol"]] = relationship(
        back_populates="usuario",
        order_by="AsignacionRol.id",
    )
    compras = relationship(
        "Compra",
        back_populates="usuario"
    )

    tickets = relationship(
        "Ticket",
        back_populates="usuario"
    )

class AsignacionRol(Base):
    __tablename__ = "asignaciones_rol"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[str] = mapped_column(String(19), nullable=False, default=_timestamp)

    usuario: Mapped["User"] = relationship(back_populates="asignaciones_rol")