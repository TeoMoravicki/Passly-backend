import uuid

# Base de datos en memoria
tickets = []
ticket_id_counter = 1

def generar_identifier():
    """Genera un identificador único para el ticket"""
    return f"TICKET-{uuid.uuid4().hex[:8].upper()}"

def get_all_tickets():
    """Obtiene todos los tickets (igual que GET /events)"""
    return tickets

def get_ticket(ticket_id: int):
    """Busca un ticket por su ID (igual que GET /events/{id})"""
    for ticket in tickets:
        if ticket["id"] == ticket_id:  # ✅ 8 espacios
            return ticket              # ✅ 12 espacios
    return None

def create_ticket(user_id: int, event_id: int):
    """Crea un nuevo ticket"""
    global ticket_id_counter

    # Generar identificador único
    identifier = generar_identifier()

    # Crear el ticket con ID autoincremental
    new_ticket = {
        "id": ticket_id_counter,
        "user_id": user_id,
        "event_id": event_id,
        "identifier": identifier
    }

    # Guardar en la "base de datos"
    tickets.append(new_ticket)
    ticket_id_counter += 1

    return new_ticket