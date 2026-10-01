from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .compras_dto import CompraCreateDTO
from .compras_service import ComprasService
from ..database.database import get_db

router = APIRouter(prefix="/compras", tags=["Compras"])

service = ComprasService()

@router.get("/")
def get_compras(db: Session = Depends(get_db)):
    return service.get_compras(db)


@router.get("/{user_id}")
def get_compra_by_user_id(user_id: int,
                db: Session = Depends(get_db)):
    return service.get_compra_by_user_id(db, user_id)

@router.post("/")
def create_compra( data: CompraCreateDTO,
    db: Session = Depends(get_db)):
    return service.create_compra(db, data)