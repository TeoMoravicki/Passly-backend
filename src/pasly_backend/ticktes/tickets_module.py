from pydantic import BaseModel

class TicketCreate(BaseModel):
    user_id: int
    event_id: int

class TicketResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    identifier: str