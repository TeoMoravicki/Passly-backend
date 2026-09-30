from sqlalchemy import Date, Time, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from  pasly_backend.database.database import Base


class Compra(Base):
    __tablename__ = "compras"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    fecha: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    monto: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    moneda: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="ARS"
    )

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"),
        nullable=False
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    evento = relationship(
        "Eventos",
        back_populates="funciones"
    )

    ticket = relationship(
        "Ticket",
        back_populates="funciones"
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
