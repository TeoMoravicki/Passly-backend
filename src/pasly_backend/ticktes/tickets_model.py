from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pasly_backend.database.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    qr: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    compra_id: Mapped[int] = mapped_column(
        ForeignKey("compras.id"),
        nullable=False
    )

    funcion_id: Mapped[int] = mapped_column(
        ForeignKey("funciones.id"),
        nullable=False
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria.id"),
        nullable=False
    )

    funcion = relationship(
        "Funcion",
        back_populates="tickets"
    )

    usuario = relationship(
        "User",
        back_populates="tickets"
    )

    categoria = relationship(
        "Categoria",
        back_populates="ticket"
    )

    compra = relationship(
        "Compra",
        back_populates="tickets"
    )