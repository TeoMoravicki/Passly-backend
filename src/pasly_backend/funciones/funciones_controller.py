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

@router.get("/id/{event_id}")
def get_funcion_by_event_id(event_id: int,
                            db: Session = Depends(get_db)
                            ):
    return service.get_funcion_by_event_id(db, event_id)


@router.post("/")
def create_event( data: FuncionCreateDTO,
    db: Session = Depends(get_db)):
    return service.create_funcion(db, data)