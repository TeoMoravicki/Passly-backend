from sqlalchemy import String, Integer, Float, Date, Time
from pydantic import BaseModel

class CompraCreateDTO(BaseModel):
    fecha: Date
    monto: int
    ticket_id: int
    funcion_id: int


class CompraResponseDTO(BaseModel):
    id: int
    fecha: Date
    monto: int
    ticket_id: int
    funcion_id: int

    model_config = {
        "from_attributes": True
    }