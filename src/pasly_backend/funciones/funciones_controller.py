from fastapi import APIRouter, HTTPException

from . import funciones_service


router = APIRouter(prefix="/funciones", tags=["Funciones"])

@router.get("/")
def get_funciones():
    return funciones_service.get_funciones()

@router.get("/evento/{evento_id}")
def get_funciones_by_evento_id(evento_id: int):
    funciones = get_funciones_by_evento(evento_id)

    if not funciones:
        raise HTTPException(
            status_code=404,
            detail="No hay funciones para este evento"
        )
    return funciones

@router.get("/{funcion_id}")
def get_funcion_by_id(funcion_id: int):
    funcion = get_funcion(funcion_id)

    if not funcion:
        raise HTTPException(
            status_code=404,
            detail="Función no encontrada"
        )
    return funcion

@router.post("/")
def create_new_funcion(funcion: FuncionCreate):
    resultado = create_funcion(
        evento_id=funcion.evento_id,
        fecha=funcion.fecha,
        horario=funcion.horario,
        capacidad_maxima=funcion.capacidad_maxima
    )

    if "error" in resultado:
        raise HTTPException(
            status_code=400,
            detail=resultado["error"]
        )
    return resultado