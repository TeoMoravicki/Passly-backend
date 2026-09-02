from fastapi import APIRouter
from schemas import Event
from eventos_controller import service


router = APIRouter(prefix="/admin/eventos", tags=["Eventos Admin (Privado)"])

@router.post("/")
def create_event(evento: Event):
    return service.create_event(evento.model_dump())

@router.put("/{event_id}")
def update_event(event_id: int, evento: Event):
    return service.update_event(event_id, evento.model_dump())

@router.delete("/{event_id}")
def delete_event(event_id: int):
    return service.delete_event(event_id)