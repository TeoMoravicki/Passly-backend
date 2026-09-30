from .database import Base, engine

from pasly_backend.categoria.categoria_model import Categoria  
from pasly_backend.compras.compras_model import Compra 
from pasly_backend.eventos.eventos_model import Eventos
from pasly_backend.funciones.funciones_model import Funcion
from pasly_backend.ticktes.tickets_model import Ticket
from pasly_backend.usuarios.usuarios_model import AsignacionRol, User


def create_tables():
    Base.metadata.create_all(bind=engine)
