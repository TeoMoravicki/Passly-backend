from pydantic import BaseModel
from typing import Literal

class EventCreateDTO(BaseModel):
    nombre: str
    descripcion: str
    capacidad_maxima: int
    lugar: str
    precio_base: int
    moneda: Literal["ARS", "USD", "EUR"] = "ARS"
    estado: str
    imagen: str



class EventResponseDTO(BaseModel):
    id: int
    nombre: str
    descripcion: str
    capacidad_maxima: int
    lugar: str
    precio_base: int
    moneda: Literal["ARS", "USD", "EUR"]
    estado: str

    model_config = {
        "from_attributes": True
    }