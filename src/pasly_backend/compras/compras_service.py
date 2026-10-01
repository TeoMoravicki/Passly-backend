from sqlalchemy.orm import Session

from pasly_backend.compras.compras_dto import CompraCreateDTO, CompraEstadoDTO
from pasly_backend.compras.compras_model import Compra
from pasly_backend.ticktes.tickets_model import Ticket


class ComprasService:

    def create_compra(
        self,
        db: Session,
        data: CompraCreateDTO
    ):
        # Buscar el ticket
        ticket = db.get(Ticket, data.ticket_id)

        if ticket is None:
            return None

        # Obtener el precio del evento a través de:
        # Ticket -> Funcion -> Evento
        precio_base = ticket.funcion.evento.precio_base


        tasas = {
            "ARS": 1,
            "USD": 1500,
            "EUR": 1750
        }

        # Convertir el precio
        monto_convertido = precio_base / tasas[data.moneda]

        compra = Compra(
            fecha=data.fecha,
            monto=round(monto_convertido, 2),
            moneda=data.moneda,
            ticket_id=data.ticket_id,
            usuario_id=data.usuario_id,
            estado=data.estado
        )

        db.add(compra)
        db.commit()
        db.refresh(compra)

        return compra

    def get_compras(self, db: Session):
        return db.query(Compra).all()

    def get_compra_by_user_id(
        self,
        db: Session,
        user_id: int
    ):
        return db.query(Compra).filter(
            Compra.usuario_id == user_id
        ).all()

    def update_estado(
            self,
            db: Session,
            compra_id: int,
            data: CompraEstadoDTO
    ):
        compra = db.get(Compra, compra_id)

        if compra is None:
            return None

        compra.estado = data.estado

        db.commit()
        db.refresh(compra)

        return compra

    def get_historial(self, db: Session, usuario_id: int):
        return (
            db.query(Compra)
            .filter(Compra.usuario_id == usuario_id)
            .all()
        )