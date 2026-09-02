from fastapi import APIRouter, HTTPException
from .tickets_module import TicketCreate
from .tickets_service import get_all_tickets, get_ticket, create_ticket

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/")
def get_tickets():
    """Obtiene todos los tickets"""
    return get_all_tickets()

@router.get("/{ticket_id}")
def get_ticket_by_id(ticket_id: int):
    """Obtiene un ticket por su ID"""
    ticket = get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

@router.post("/")
def create_new_ticket(ticket: TicketCreate):
    """Crea un nuevo ticket"""
    return create_ticket(ticket.user_id, ticket.event_id)