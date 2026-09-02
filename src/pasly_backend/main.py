from fastapi import FastAPI

from .database.models import create_tables
from .eventos.eventos_controller import router as eventos_router
from .ticktes.tickets_controller import router as tickets_router
from .usuarios.usuarios_controller import router as usuarios_router

app = FastAPI()


app.include_router(eventos_router)
app.include_router(tickets_router)
app.include_router(usuarios_router)

create_tables()

@app.get("/")
def root():
    return {"message": "API funcionando"}