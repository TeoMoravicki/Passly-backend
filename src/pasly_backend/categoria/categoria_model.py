from sqlalchemy import String, Integer, Float, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from  pasly_backend.database.database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    precio: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    lugar: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    funciones = relationship(
        "Funcion",
        back_populates="evento"
    )