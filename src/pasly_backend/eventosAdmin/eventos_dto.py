from pydantic import BaseModel

class EventoDTO(BaseModel):
    nombre: str
    horario: str
    entradasdisponibles: int
    descripcion: str
    lugar: str
    fecha: str
    precio: int
    categoria: str
    estado: str
    imagen: str


class CompraCreate(BaseModel):
    event_id: int
    cantidad_entradas: int
    categoria: str