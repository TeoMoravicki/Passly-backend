from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .eventos_dto import EventCreateDTO
from .eventos_service import EventosService
from ..database.database import get_db

router = APIRouter(prefix="/eventos", tags=["Eventos"])

service = EventosService()

@router.get("/")
def get_events():
    return service.get_events()


@router.get("/{event_id}")
def get_event(event_id: int):
    return service.get_event(event_id)

@router.post("/")
def create_event( data: EventCreateDTO,
    db: Session = Depends(get_db)):
    return service.create_event(db, data)