# dtos/ticket_dto.py

from pydantic import BaseModel


class TicketCreateDTO(BaseModel):
    usuario_id: int
    funcion_id: int
    categoria_id: int

class TicketResponseDTO(BaseModel):
    id: int
    qr: str
    estado: str
    funcion_id: int
    usuario_id: int
    categoria_id: int

    model_config = {
        "from_attributes": True
    }