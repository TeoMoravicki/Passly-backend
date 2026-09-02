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