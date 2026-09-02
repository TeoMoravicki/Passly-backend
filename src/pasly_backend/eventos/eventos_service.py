class EventosService:
    def __init__(self):
        self.eventos = [
            {
                "id": 1,
                "nombre": "Concierto",
                "horario": "20:00",
                "entradasdisponibles": 100,
                "descripcion": "Evento musical",
                "lugar": "Estadio",
                "fecha": "2026-10-15",
                "precio": 5000,
                "categoria": "Musica",
                "estado": "Activo",
                "imagen": "concierto.jpg"
            }
        ]

    def get_events(self):
      return self.eventos

    def get_event(self, event_id: int):
        for evento in self.eventos:
            if evento["id"] == event_id:
                return evento
        return {"error": "Evento no encontrado"}