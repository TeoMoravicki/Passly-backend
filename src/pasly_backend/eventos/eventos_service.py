import os
from sqlalchemy.orm import Session

from pasly_backend.eventos.eventos_dto import EventCreateDTO
from pasly_backend.eventos.eventos_model import Eventos

os.makedirs("static", exist_ok=True)

class EventosService:
    def create_event(self, db: Session, data: EventCreateDTO):
        evento = Eventos(
            nombre=data.nombre,
            descripcion=data.descripcion,
            capacidad_maxima=data.capacidad_maxima,
            lugar=data.lugar,
            precio_base=data.precio_base,
            estado=data.estado,
            imagen=data.imagen,
        )

        db.add(evento)
        db.commit()
        db.refresh(evento)

        return evento

    def get_event_by_id(
            self,
            db: Session,
            event_id: int
    ):
        return db.get(Eventos, event_id)

    def get_events(self, db: Session):
        return db.get(Eventos)