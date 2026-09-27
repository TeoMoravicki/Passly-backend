from pydantic import BaseModel


class CategoriaCreateDTO(BaseModel):
    nombre: str
    precio: int
    lugar: str
