from sqlalchemy import String, Integer, Float, Date, Time
from pydantic import BaseModel

class FuncionCreateDTO(BaseModel):
    evento_id: int
    fecha: Date
    horario: Time
    capacidad_maxima: int

class FuncionResponseDTO(BaseModel):
    id: int
    evento_id: int
    fecha: Date
    horario: Time
    capacidad_maxima: int
    entradas_disponibles: int
    estado: str

    model_config = {
        "from_attributes": True
    }