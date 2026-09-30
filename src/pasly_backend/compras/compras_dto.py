from datetime import date

from sqlalchemy import String, Integer, Float, Date, Time
from pydantic import BaseModel

class CompraCreateDTO(BaseModel):
    fecha: date
    monto: int
    ticket_id: int
    funcion_id: int


class CompraResponseDTO(BaseModel):
    id: int
    fecha: date
    monto: int
    ticket_id: int
    funcion_id: int
    estado: str

    model_config = {
        "from_attributes": True
    }