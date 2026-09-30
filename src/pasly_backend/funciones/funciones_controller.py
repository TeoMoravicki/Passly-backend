from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from . import funciones_service
from .funciones_dto import FuncionCreateDTO
from ..database.database import get_db

router = APIRouter(prefix="/funciones", tags=["Funciones"])

service = funciones_service.FuncionesService()


@router.get("/")
def get_funciones(db: Session = Depends(get_db)):
    return service.get_funciones(db)


@router.get("/evento/{evento_id}")
def get_funciones_by_evento_id(
    evento_id: int,
    db: Session = Depends(get_db)
):
    return service.get_funciones_by_evento_id(db, evento_id)


@router.get("/{funcion_id}")
def get_funcion_by_id(
    funcion_id: int,
    db: Session = Depends(get_db)
):
    funcion = service.get_funcion_by_id(db, funcion_id)

    if not funcion:
        raise HTTPException(
            status_code=404,
            detail="Función no encontrada"
        )

    return funcion


@router.post("/")
def create_funcion(
    data: FuncionCreateDTO,
    db: Session = Depends(get_db)
):
    return service.create_funcion(db, data)