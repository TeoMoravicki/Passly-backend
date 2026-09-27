from .database import Base, engine

from pasly_backend.usuarios.usuarios_model import AsignacionRol, User

def create_tables():
    Base.metadata.create_all(bind=engine)