from datetime import date
from pydantic import BaseModel
from typing import Literal


class CompraCreateDTO(BaseModel):
    fecha: date
    moneda: Literal["ARS", "USD", "EUR"] = "ARS"
    ticket_id: int
    usuario_id: int
    estado: str = "PENDIENTE"


class CompraResponseDTO(BaseModel):
    id: int
    fecha: date
    monto: int
    moneda: str
    ticket_id: int
    usuario_id: int

    model_config = {
        "from_attributes": True
    }

class CompraEstadoDTO(BaseModel):
    estado: str