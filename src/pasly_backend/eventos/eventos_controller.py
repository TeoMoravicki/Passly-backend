from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .eventos_dto import EventCreateDTO, EventUpdateDTO
from .eventos_service import EventosService
from ..database.database import get_db

router = APIRouter(prefix="/eventos", tags=["Eventos"])

service = EventosService()


@router.get("/")
def get_events(db: Session = Depends(get_db)):
    return service.get_events(db)


@router.get("/{event_id}")
def get_event_by_id(
    event_id: int,
    db: Session = Depends(get_db)
):
    return service.get_event_by_id(db, event_id)


@router.post("/")
def create_event(
    data: EventCreateDTO,
    db: Session = Depends(get_db)
):
    return service.create_event(db, data)


@router.put("/{event_id}")
def update_event(
    event_id: int,
    data: EventUpdateDTO,
    db: Session = Depends(get_db)
):
    return service.update_event(db, event_id, data)


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    return service.delete_event(db, event_id)