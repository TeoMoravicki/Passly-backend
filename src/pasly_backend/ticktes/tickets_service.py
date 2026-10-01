import uuid

tickets = []
ticket_id_counter = 1

def generar_identifier():
    return f"TICKET-{uuid.uuid4().hex[:8].upper()}"

def get_all_tickets():
    return tickets

def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    return None

def get_tickets_by_compra(compra_id: int):
    resultado = []
    for ticket in tickets:
        if ticket["compra_id"] == compra_id:
            resultado.append(ticket)
    return resultado


def create_ticket(user_id: int, funcion_id: int, compra_id: int):
    global ticket_id_counter

    identifier = generar_identifier()

    new_ticket = {
        "id": ticket_id_counter,
        "user_id": user_id,
        "funcion_id": funcion_id,
        "compra_id": compra_id,
        "identifier": identifier,
        "estado": "ACTIVO"
    }

    tickets.append(new_ticket)

    ticket_id_counter += 1
    return new_ticket


def update_ticket_estado(ticket_id: int, nuevo_estado: str):
    estados_validos = ["ACTIVO", "USADO", "CANCELADO"]
    
    if nuevo_estado.upper() not in estados_validos:
        return {"error": "Estado de ticket no válido"}

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["estado"] = nuevo_estado.upper()
            return ticket
    return None