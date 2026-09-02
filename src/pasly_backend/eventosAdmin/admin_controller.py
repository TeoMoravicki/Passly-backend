from fastapi import APIRouter
from .eventos_dto import EventoDTO
from ..eventos.eventos_service import EventosService as service


router = APIRouter(prefix="/admin/eventos", tags=["Eventos Admin (Privado)"])

@router.post("/")
def create_event(evento: EventoDTO):
    return service.create_event(evento.model_dump())

@router.put("/{event_id}")
def update_event(event_id: int, evento: EventoDTO):
    return service.update_event(event_id, evento.model_dump())

@router.delete("/{event_id}")
def delete_event(event_id: int):
    return service.delete_event(event_id)