from datetime import date
from decimal import Decimal

from sqlalchemy import String, ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pasly_backend.database.database import Base


class Compra(Base):
    __tablename__ = "compras"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    monto: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    moneda: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="ARS"
    )

    tasa_utilizada: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"),
        nullable=False
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    ticket = relationship(
        "Ticket",
        back_populates="compra"
    )

    usuario = relationship(
        "User",
        back_populates="compras"
    )