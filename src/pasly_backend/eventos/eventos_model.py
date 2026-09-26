from sqlalchemy import String, Integer, Float, Date, Time
from sqlalchemy.orm import Mapped, mapped_column

from  pasly_backend.database.database import Base


class Eventos(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    horario: Mapped[Time] = mapped_column(
        Time,
        nullable=False
    )

    entradas_disponibles: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    lugar: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    fecha: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    precio: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    categoria_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    imagen: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )