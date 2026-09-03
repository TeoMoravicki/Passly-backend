from pydantic import BaseModel

class TicketCreate(BaseModel):
    user_id: int
    funcion_id: int
    compra_id: int

class TicketResponse(BaseModel):
    id: int
    user_id: int
    funcion_id: int
    compra_id: int
    identifier: str
    estado: str