from datetime import date
from decimal import Decimal
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
    monto: Decimal
    moneda: str
    tasa_utilizada: Decimal
    ticket_id: int
    usuario_id: int

    model_config = {
        "from_attributes": True
    }


class CompraEstadoDTO(BaseModel):
    estado: str


class ReservaCreateDTO(BaseModel):
    usuario_id: int
    funcion_id: int
    cantidad: int