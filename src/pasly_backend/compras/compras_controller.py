from fastapi import APIRouter
from pasly_backend.eventos.eventos_dto import CompraCreate
from pasly_backend.eventos.eventos_service import EventosService as service

router = APIRouter(prefix="/compras", tags=["Proceso de Compras"])

@router.post("/")
def realizar_compra(compra: CompraCreate):
    resultado = service.procesar_compra(compra.model_dump())
    return resultado