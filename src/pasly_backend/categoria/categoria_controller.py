from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .categoria_dto import CategoriaCreateDTO
from .categoria_service import CategoriaService
from ..database.database import get_db

router = APIRouter(prefix="/categoria", tags=["Categoria"])

service = CategoriaService()

@router.get("/")
def get_categoria(db: Session = Depends(get_db)):
    return service.get_categorias(db)


@router.get("/{event_id}")
def get_categoria_by_id(event_id: int,
                db: Session = Depends(get_db)):
    return service.get_categoria_by_id(db, event_id)

@router.post("/")
def create_categoria( data: CategoriaCreateDTO,
    db: Session = Depends(get_db)):
    return service.create_categoria(db, data)