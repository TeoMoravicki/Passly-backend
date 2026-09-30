import os
from sqlalchemy.orm import Session

from pasly_backend.eventos.eventos_dto import EventCreateDTO, EventUpdateDTO
from pasly_backend.eventos.eventos_model import Eventos

os.makedirs("static", exist_ok=True)


class EventosService:

    # CREATE
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
        return db.query(Eventos).all()


    def update_event(
            self,
            db: Session,
            event_id: int,
            data: EventUpdateDTO
    ):
        evento = db.get(Eventos, event_id)

        if evento is None:
            return None

        evento.nombre = data.nombre
        evento.descripcion = data.descripcion
        evento.capacidad_maxima = data.capacidad_maxima
        evento.lugar = data.lugar
        evento.precio_base = data.precio_base
        evento.estado = data.estado
        evento.imagen = data.imagen

        db.commit()
        db.refresh(evento)

        return evento


    def delete_event(
            self,
            db: Session,
            event_id: int
    ):
        evento = db.get(Eventos, event_id)

        if evento is None:
            return None

        db.delete(evento)
        db.commit()

        return evento