from sqlalchemy import String, Integer, Float, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    descripcion: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    capacidad_maxima: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    lugar: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    precio_base: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    moneda: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="ARS"
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    imagen: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    funciones = relationship(
        "Funcion",
        back_populates="evento"
    )