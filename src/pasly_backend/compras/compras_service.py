from sqlalchemy.orm import Session

from pasly_backend.compras.compras_dto import CompraCreateDTO
from pasly_backend.compras.compras_model import Compra
from pasly_backend.funciones.funciones_dto import FuncionCreateDTO
from pasly_backend.funciones.funciones_model import Funcion

class ComprasService:
    def create_compra(self, db: Session,
                       data: CompraCreateDTO):
        compra = Compra(

        )
        db.add(compra)
        db.commit()
        db.refresh(compra)
        return compra

    #def get_funcion_by_evento_id(self, evento_id: int) -> Funcion:

    def get_compras(self, db: Session):
        return db.get(Compra)


    def get_compra_by_user_id(self, db: Session, user_id: int

    ):
        return db.get(Compra, user_id)

    def get_historial(self, db: Session, usuario_id: int):
        return (
            db.query(Compra)
            .filter(Compra.usuario_id == usuario_id)
            .all()
        )

    def cancelar_compra(
            self,
            db: Session,
            compra_id: int
    ):
        compra = db.get(Compra, compra_id)

        if compra is None:
            return None

        if compra.estado == "CANCELADA":
            return compra

        compra.estado = "CANCELADA"

        db.commit()
        db.refresh(compra)

        return compra