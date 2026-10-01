from sqlalchemy import String, Date, Time, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pasly_backend.database.database import Base


class Funcion(Base):
    __tablename__ = "funciones"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    evento_id: Mapped[int] = mapped_column(
        ForeignKey("eventos.id"),
        nullable=False
    )

    hora: Mapped[Time] = mapped_column(
        Time,
        nullable=False
    )

    dia: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    entradas_disponibles: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    evento = relationship(
        "Eventos",
        back_populates="funciones"
    )