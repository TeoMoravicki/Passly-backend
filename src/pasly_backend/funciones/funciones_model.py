from sqlalchemy import Date, Time, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from  pasly_backend.database.database import Base


class Funcion(Base):
    __tablename__ = "funciones"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    fecha: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    horario: Mapped[Time] = mapped_column(
        Time,
        nullable=False
    )

    capacidad_maxima: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    evento_id: Mapped[int] = mapped_column(
        ForeignKey("eventos.id"),
        nullable=False
    )

    evento = relationship(
        "Evento",
        back_populates="funciones"
    )