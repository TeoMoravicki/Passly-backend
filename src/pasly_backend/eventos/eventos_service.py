import qrcode
import os

os.makedirs("static", exist_ok=True)

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
        email = compra_data["comprador_email"]

        # Buscar el evento
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
            return {"error": f"Rechazar compra: Supera el límite permitido ({LIMITE_MAXIMO} entradas)"}

        # Calcular total y reservar stock
        total_pagar = cantidad * evento_encontrado["precio"]
        evento_encontrado["entradasdisponibles"] -= cantidad

        compra_id = len(evento_encontrado) + 1500  # ID simulado de compra único

        # 1. Crear el texto que contendrá el QR con toda la info de la compra
        info_qr = (
            f"ID_COMPRA: {compra_id} | "
            f"EVENTO: {evento_encontrado['nombre']} | "
            f"CATEGORIA: {categoria_seleccionada} | "
            f"CANTIDAD: {cantidad} | "
            f"TOTAL: ${total_pagar} | "
            f"COMPRADOR: {email}"
        )

        # 2. Generar la imagen física del QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(info_qr)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # 3. Guardar la imagen QR en la carpeta static
        ruta_qr = f"static/qr_compra_{compra_id}.png"
        img.save(ruta_qr)

        # 4. Retornar el comprobante con la ruta del QR generado
        return {
            "estado": "COMPRA OK",
            "mensaje": "¡Entradas compradas y comprobante generado con éxito!",
            "comprobante": {
                "compra_id": compra_id,
                "evento": evento_encontrado["nombre"],
                "categoria": categoria_seleccionada,
                "entradas_compradas": cantidad,
                "total_abonado": f"${total_pagar}",
                "comprador": email,
                "stock_remanente": evento_encontrado['entradasdisponibles']
            },
            "qr_generado": {
                "contenido_codificado": info_qr,
                "archivo_qr": ruta_qr  # Ruta física del QR guardado en tu proyecto
            }
        }