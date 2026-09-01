class EventosService:

    def get_events(self):
        return {"message": "Lista de eventos"}

    def get_event(self, event_id: int):
        return {"message": f"Evento {event_id}"}

