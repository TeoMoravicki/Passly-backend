from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Literal

from .eventos_dto import EventCreateDTO
from .eventos_service import EventosService
from ..database.database import get_db

router = APIRouter(prefix="/eventos", tags=["Eventos"])

service = EventosService()

@router.get("/")
def get_events(db: Session = Depends(get_db)):
    return service.get_events(db)


@router.get("/{event_id}")
def get_event_by_id(event_id: int,
                db: Session = Depends(get_db)):
    return service.get_event_by_id(db, event_id)

@router.post("/")
def create_event( data: EventCreateDTO,
    db: Session = Depends(get_db)):
    return service.create_event(db, data)


@router.get("/{event_id}/precio/{moneda}")
def convertir_precio(
    event_id: int,
    moneda: Literal["ARS", "USD", "EUR"],
    db: Session = Depends(get_db)
):
    return service.convertir_precio(db, event_id, moneda)