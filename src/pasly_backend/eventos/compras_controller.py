from fastapi import APIRouter
from pasly_backend.eventosAdmin.eventos_dto import EventoDTO, CompraCreate
from pasly_backend.eventos.eventos_service import EventosService as service

router = APIRouter(prefix="/compras", tags=["Proceso de Compras"])

@router.post("/")
def realizar_compra(compra: CompraCreate):
    resultado = service.procesar_compra(compra.model_dump())
    return resultado