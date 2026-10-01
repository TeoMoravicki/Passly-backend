from pydantic import BaseModel
from datetime import date, time


class FuncionCreateDTO(BaseModel):
    evento_id: int
    dia: date
    hora: time
    entradas_disponibles: int
    estado: str = "ACTIVO"


class FuncionResponseDTO(BaseModel):
    id: int
    evento_id: int
    dia: date
    hora: time
    entradas_disponibles: int
    estado: str

    model_config = {
        "from_attributes": True
    }