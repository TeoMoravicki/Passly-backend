from fastapi import APIRouter, HTTPException

from .tickets_dto import TicketCreateDTO
from .tickets_service import (
    get_all_tickets,
    get_ticket,
    create_ticket,
    get_tickets_by_compra
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/")
def get_tickets():
    return get_all_tickets()

@router.get("/compra/{compra_id}")
def get_tickets_by_compra_id(compra_id: int):
    tickets = get_tickets_by_compra(compra_id)

    if not tickets:
        raise HTTPException(
            status_code=404,
            detail="No hay tickets para esta compra"
        )
    return tickets

@router.get("/{ticket_id}")
def get_ticket_by_id(ticket_id: int):
    ticket = get_ticket(ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket no encontrado"
        )
    return ticket

@router.post("/")
def create_new_ticket(ticket: TicketCreateDTO):
    return create_ticket(
        ticket.usuario_id,
        ticket.funcion_id,
        ticket.categoria_id
    )