import os
from sqlalchemy.orm import Session

from pasly_backend.categoria.categoria_model import Categoria
from pasly_backend.categoria.categoria_dto import CategoriaCreateDTO


os.makedirs("static", exist_ok=True)

class CategoriaService:
    def create_categoria(self, db: Session, data: CategoriaCreateDTO):
        categoria = Categoria(
            precio=data.precio,
            lugar=data.lugar,
        )

        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        return categoria

    def get_categoria_by_id(self, db: Session, id: int
    ):
        return db.get(Categoria, id)

    def get_categorias(self, db: Session):
        return db.get(Categoria)