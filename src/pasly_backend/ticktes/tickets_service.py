from .tickets_module import TicketCreate, TicketResponse


class TicketsService:

    def get_ticket(self, ticket_id: int):
        return {"message": f"Ticket {ticket_id}"} 

    def create_ticket(self, ticket: TicketCreate):

        new_ticket = TicketResponse(
            id=1,
            user_id=ticket.user_id,
            event_id=ticket.event_id,
            identifier="TICKET-1"
        )
        return new_ticket