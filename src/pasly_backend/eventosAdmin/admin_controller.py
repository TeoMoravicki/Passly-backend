import os
from fastapi import APIRouter, UploadFile, File, Form
from .eventos_dto import EventoDTO
from ..eventos.eventos_service import EventosService as service


router = APIRouter(prefix="/admin/eventos", tags=["Eventos Admin (Privado)"])


@router.post("/")
async def create_event(
        nombre: str = Form(...),
        horario: str = Form(...),
        entradasdisponibles: int = Form(...),
        descripcion: str = Form(...),
        lugar: str = Form(...),
        fecha: str = Form(...),
        precio: int = Form(...),
        categoria: str = Form(...),
        estado: str = Form(...),
        imagen: UploadFile = File(...)  # <--- Aquí recibes el archivo real
):
    # 1. Guardar la imagen físicamente en el disco
    ruta_archivo = f"static/{imagen.filename}"
    contenido = await imagen.read()

    with open(ruta_archivo, "wb") as buffer:
        buffer.write(contenido)

    # 2. Armar el diccionario con la ruta de la imagen ya guardada
    evento_data = {
        "nombre": nombre,
        "horario": horario,
        "entradasdisponibles": entradasdisponibles,
        "descripcion": descripcion,
        "lugar": lugar,
        "fecha": fecha,
        "precio": precio,
        "categoria": categoria,
        "estado": estado,
        "imagen": ruta_archivo  # Se guarda la ruta local del archivo
    }

    return service.create_event(evento_data)


@router.put("/{event_id}")
async def update_event(
        event_id: int,
        nombre: str = Form(...),
        horario: str = Form(...),
        entradasdisponibles: int = Form(...),
        descripcion: str = Form(...),
        lugar: str = Form(...),
        fecha: str = Form(...),
        precio: int = Form(...),
        categoria: str = Form(...),
        estado: str = Form(...),
        imagen: UploadFile = File(...)
):
    ruta_archivo = f"static/{imagen.filename}"
    contenido = await imagen.read()
    with open(ruta_archivo, "wb") as buffer:
        buffer.write(contenido)

    evento_data = {
        "nombre": nombre,
        "horario": horario,
        "entradasdisponibles": entradasdisponibles,
        "descripcion": descripcion,
        "lugar": lugar,
        "fecha": fecha,
        "precio": precio,
        "categoria": categoria,
        "estado": estado,
        "imagen": ruta_archivo
    }
    return service.update_event(event_id, evento_data)


@router.delete("/{event_id}")
def delete_event(event_id: int):
    return service.delete_event(event_id)