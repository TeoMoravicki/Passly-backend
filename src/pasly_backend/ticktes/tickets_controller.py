from fastapi import APIRouter
from .tickets_service import TicketsService
from .tickets_module import TicketCreate


router = APIRouter(prefix="/tickets", tags=["Tickets"])

service = TicketsService()


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int):
    return service.get_ticket(ticket_id)


@router.post("/")
def create_ticket(ticket: TicketCreate):
    return service.create_ticket(ticket)