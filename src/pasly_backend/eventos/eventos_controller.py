from fastapi import APIRouter
from .eventos_service import EventosService

router = APIRouter(prefix="/eventos", tags=["Eventos"])

service = EventosService()


@router.get("/")
def get_events():
    return service.get_events()


@router.get("/{event_id}")
def get_event(event_id: int):
    return service.get_event(event_id)


@router.post("/")
def create_event(name: str):
    return service.create_event(name)