from pydantic import BaseModel

class FuncionCreate(BaseModel):
    evento_id: int
    fecha: str
    horario: str
    capacidad_maxima: int

class FuncionResponse(BaseModel):
    id: int
    evento_id: int
    fecha: str
    horario: str
    capacidad_maxima: int
    entradas_disponibles: int
    estado: str