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
            moneda=data.moneda,
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

    def convertir_precio(
        self,
        db: Session,
        event_id: int,
        moneda: str
    ):
        evento = db.get(Eventos, event_id)

        if evento is None:
            return None

        tasas = {
            "ARS": 1,
            "USD": 1500,
            "EUR": 1750
        }

        precio_convertido = evento.precio_base / tasas[moneda]

        return {
            "precio_base_ars": evento.precio_base,
            "moneda": moneda,
            "precio_convertido": round(precio_convertido, 2)
        }
