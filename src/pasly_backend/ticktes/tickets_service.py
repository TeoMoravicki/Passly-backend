import uuid

from sqlalchemy.orm import Session

from pasly_backend.ticktes.tickets_model import Ticket


def generar_identifier():
    return f"TICKET-{uuid.uuid4().hex[:8].upper()}"


def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def get_ticket(db: Session, ticket_id: int):
    return db.get(Ticket, ticket_id)


def create_ticket(
    db: Session,
    user_id: int,
    funcion_id: int,
    categoria_id: int
):
    identifier = generar_identifier()

    new_ticket = Ticket(
        qr=identifier,
        estado="ACTIVO",
        funcion_id=funcion_id,
        usuario_id=user_id,
        categoria_id=categoria_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


def update_ticket_estado(
    db: Session,
    ticket_id: int,
    nuevo_estado: str
):
    estados_validos = ["ACTIVO", "USADO", "CANCELADO"]

    if nuevo_estado.upper() not in estados_validos:
        return {"error": "Estado de ticket no válido"}

    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        return None

    ticket.estado = nuevo_estado.upper()

    db.commit()
    db.refresh(ticket)

    return ticket