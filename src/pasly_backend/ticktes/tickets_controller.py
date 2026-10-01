from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .tickets_dto import TicketCreateDTO
from .tickets_service import (
    get_all_tickets,
    get_ticket,
    create_ticket
)
from ..database.database import get_db


router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/")
def get_tickets(db: Session = Depends(get_db)):
    return get_all_tickets(db)


@router.get("/{ticket_id}")
def get_ticket_by_id(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = get_ticket(db, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket no encontrado"
        )

    return ticket


@router.post("/")
def create_new_ticket(
    ticket: TicketCreateDTO,
    db: Session = Depends(get_db)
):
    return create_ticket(
        db,
        ticket.usuario_id,
        ticket.funcion_id,
        ticket.categoria_id
    )