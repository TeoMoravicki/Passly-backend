from fastapi import FastAPI

from .database.models import create_tables
from .eventos.eventos_controller import router as eventos_router
from .ticktes.tickets_controller import router as tickets_router
from .funciones.funciones_controller import router as funciones_router

app = FastAPI()


app.include_router(eventos_router)
app.include_router(tickets_router)
app.include_router(funciones_router)

create_tables()

@app.get("/")
def root():
    return {"message": "API funcionando"}