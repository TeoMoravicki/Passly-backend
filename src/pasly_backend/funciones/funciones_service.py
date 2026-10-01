from sqlalchemy.orm import Session

from pasly_backend.funciones.funciones_dto import FuncionCreateDTO
from pasly_backend.funciones.funciones_model import Funcion


class FuncionesService:

    def create_funcion(self, db: Session, data: FuncionCreateDTO):
        funcion = Funcion(
            evento_id=data.evento_id,
            dia=data.dia,
            hora=data.hora,
            entradas_disponibles=data.entradas_disponibles,
            estado=data.estado
        )

        db.add(funcion)
        db.commit()
        db.refresh(funcion)

        return funcion

    def get_funciones(self, db: Session):
        return db.query(Funcion).all()

    def get_funcion_by_id(self, db: Session, funcion_id: int):
        return db.get(Funcion, funcion_id)

    def get_funciones_by_evento_id(self, db: Session, evento_id: int):
        return (
            db.query(Funcion)
            .filter(Funcion.evento_id == evento_id)
            .all()
        )