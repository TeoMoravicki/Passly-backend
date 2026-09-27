from pydantic import BaseModel


class EventCreateDTO(BaseModel):
    nombre: str
    descripcion: str
    capacidad_maxima: int
    lugar: str
    precio_base: int
    estado: str


class EventResponseDTO(BaseModel):
    id: int
    nombre: str
    descripcion: str
    capacidad_maxima: int
    lugar: str
    precio_base: int
    estado: str

    model_config = {
        "from_attributes": True
    }