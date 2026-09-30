from sqlalchemy import String, Integer, Float, Date, Time
from pydantic import BaseModel
from datetime import date, time

class FuncionCreateDTO(BaseModel):
    evento_id: int
    fecha: date
    horario: time
    capacidad_maxima: int

class FuncionResponseDTO(BaseModel):
    id: int
    evento_id: int
    fecha: date
    horario: time
    capacidad_maxima: int
    entradas_disponibles: int
    estado: str

    model_config = ConfigDict(from_attributes=True)