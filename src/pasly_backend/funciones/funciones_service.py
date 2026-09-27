from sqlalchemy.orm import Session
from pasly_backend.funciones.funciones_dto import FuncionCreateDTO
from pasly_backend.funciones.funciones_model import Funcion

class FuncionesService:
    def create_funcion(self, db: Session,
                       data: FuncionCreateDTO):
        funcion = Funcion(
            evento_id=data.evento_id,
            fecha=data.fecha,
            horario=data.horario,
            capacidad_maxima=data.capacidad_maxima,
        )
        db.add(funcion)
        db.commit()
        db.refresh(funcion)
        return funcion

    #def get_funcion_by_evento_id(self, evento_id: int) -> Funcion:

    def get_funciones(self, db: Session):
        return db.get(Funcion)


    def get_funcion_by_event_id(
            self,
            db: Session,
            event_id: int
    ):
        return db.get(Funcion, event_id)