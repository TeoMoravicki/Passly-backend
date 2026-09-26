from sqlalchemy import String, Integer, Float, Date, Time
from pydantic import BaseModel


class EventCreateDTO(BaseModel):
    nombre: str
    horario: Time
    entradas_disponibles: int
    descripcion: str
    lugar: str
    fecha: Date
    precio: int
    categoria_id: str
    estado: str


class EventResponseDTO(BaseModel):
    id: int
    nombre: str
    horario: Time
    entradas_disponibles: int
    descripcion: str | None
    lugar: str
    fecha: Date
    precio: int
    categoria_id: int
    estado: str

    model_config = {
        "from_attributes": True
    }