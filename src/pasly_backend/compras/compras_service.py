import json
import uuid
from sqlalchemy.orm import Session

from pasly_backend.redis_config.redis_client import redis_client
from pasly_backend.compras.compras_dto import CompraCreateDTO, CompraEstadoDTO
from pasly_backend.compras.compras_model import Compra
from pasly_backend.ticktes.tickets_model import Ticket
from pasly_backend.funciones.funciones_model import Funcion
from pasly_backend.rabbitmq.rabbitmq_client import publicar_compra_confirmada

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


        print("TICKET:", ticket.id)
        print("FUNCION:", ticket.funcion)
        print("EVENTO:", ticket.funcion.evento)

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

    def get_compra_by_id(
            self,
            db: Session,
            compra_id: int
    ):
        return db.get(Compra, compra_id)

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

        if data.estado == "CONFIRMADA":
            publicar_compra_confirmada({
                "evento_id": str(uuid.uuid4()),
                "tipo": "CompraConfirmada",
                "compra_id": compra.id,
                "usuario_id": compra.usuario_id,
                "ticket_id": compra.ticket_id,
                "monto": compra.monto,
                "estado": compra.estado
            })

        return compra

    def get_historial(self, db: Session, usuario_id: int):
        return (
            db.query(Compra)
            .filter(Compra.usuario_id == usuario_id)
            .all()
        )

    def reservar_entradas(
            self,
            db: Session,
            data
    ):
        if data.cantidad <= 0:
            return {"error": "La cantidad debe ser mayor a cero"}

        funcion = db.get(Funcion, data.funcion_id)

        if funcion is None:
            return {"error": "La funcion no existe"}

        clave_stock = f"reservadas:funcion:{data.funcion_id}"

        reservadas = int(redis_client.get(clave_stock) or 0)

        disponibles = funcion.entradas_disponibles - reservadas

        if disponibles < data.cantidad:
            return {"error": "No hay suficientes entradas"}

        reserva_id = str(uuid.uuid4())

        reserva = {
            "usuario_id": data.usuario_id,
            "funcion_id": data.funcion_id,
            "cantidad": data.cantidad,
            "estado": "PENDIENTE"
        }

        redis_client.incrby(clave_stock, data.cantidad)

        redis_client.set(
            f"reserva:{reserva_id}",
            json.dumps(reserva),
            ex=600
        )

        return {
            "reserva_id": reserva_id,
            "mensaje": "Reserva temporal creada",
            "expira_en": 600
        }

    def confirmar_reserva(
            self,
            db: Session,
            reserva_id: str
    ):
        clave = f"reserva:{reserva_id}"

        datos = redis_client.get(clave)

        if datos is None:
            return {"error": "La reserva no existe o expiro"}

        reserva = json.loads(datos)

        funcion = db.get(
            Funcion,
            reserva["funcion_id"]
        )

        if funcion is None:
            return {"error": "La funcion no existe"}

        cantidad = reserva["cantidad"]

        if funcion.entradas_disponibles < cantidad:
            return {"error": "Stock insuficiente"}

        funcion.entradas_disponibles -= cantidad

        db.commit()
        db.refresh(funcion)

        redis_client.decrby(
            f"reservadas:funcion:{funcion.id}",
            cantidad
        )

        redis_client.delete(clave)

        return {
            "mensaje": "Reserva confirmada",
            "entradas_disponibles": funcion.entradas_disponibles
        }