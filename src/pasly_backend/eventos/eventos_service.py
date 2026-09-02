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

    def create_event(self, evento_data: dict):
        self.eventos.append(evento_data)
        return {"message": "Evento creado exitosamente", "evento": evento_data}

    def update_event(self, event_id: int, evento_data: dict):
        for i, evento in enumerate(self.eventos):
            if evento["id"] == event_id:
                self.eventos[i].update(evento_data)
                return {"message": "Evento actualizado", "evento": self.eventos[i]}
        return {"error": "Evento no encontrado"}

    def delete_event(self, event_id: int):
        for i, evento in enumerate(self.eventos):
            if evento["id"] == event_id:
                eliminado = self.eventos.pop(i)
                return {"message": "Evento eliminado", "evento": eliminado}
        return {"error": "Evento no encontrado"}