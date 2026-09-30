from datetime import date, time
from pydantic import BaseModel, ConfigDict


class FuncionCreateDTO(BaseModel):
    evento_id: int
    dia: date
    hora: time
    entradas_disponibles: int
    estado: str


class FuncionResponseDTO(BaseModel):
    id: int
    evento_id: int
    dia: date
    hora: time
    entradas_disponibles: int
    estado: str

    model_config = ConfigDict(from_attributes=True)