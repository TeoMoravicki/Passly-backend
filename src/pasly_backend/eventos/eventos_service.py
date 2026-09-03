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

    def procesar_compra(self, compra_data: dict):
        event_id = compra_data["event_id"]
        cantidad = compra_data["cantidad"]
        categoria_seleccionada = compra_data["categoria"]

        evento_encontrado = None
        for evento in self.eventos:
            if evento["id"] == event_id:
                evento_encontrado = evento
                break

        if not evento_encontrado:
            return {"error": "Rechazar compra: Evento no encontrado"}


        if evento_encontrado["categoria"].lower() != categoria_seleccionada.lower():
            return {"error": "Rechazar compra: La categoría no coincide con el evento"}

        stock_actual = evento_encontrado["entradasdisponibles"]

        if stock_actual <= 0 or stock_actual < cantidad:
            return {"error": "Rechazar compra: No hay stock suficiente"}

        LIMITE_MAXIMO = 5
        if cantidad > LIMITE_MAXIMO:
            return {"error": f"Rechazar compra: Supera el límite permitido por compra ({LIMITE_MAXIMO} entradas)"}


        total_pagar = cantidad * evento_encontrado["precio"]


        evento_encontrado["entradasdisponibles"] -= cantidad

        compra_id = 999
        resumen_compra = {
            "compra_id": compra_id,
            "evento": evento_encontrado["nombre"],
            "categoria": categoria_seleccionada,
            "cantidad": cantidad,
            "total_calculado": total_pagar,
            "estado_stock": f"Stock actualizado. Quedan {evento_encontrado['entradasdisponibles']}",
            "ticket_generado": f"TICKET-EV{event_id}-Q{cantidad}",
            "qr_code": f"https://api.qrserver.com/v1/create-qr-code/?data=TICKET-{compra_id}",
            "comprobante": "Emitido correctamente",
            "status": "COMPRA OK"
        }

        return resumen_compra