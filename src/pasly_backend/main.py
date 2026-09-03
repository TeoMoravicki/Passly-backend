from fastapi import FastAPI
from .database.models import create_tables
from .eventos.eventos_controller import router as eventos_router
from .eventosAdmin.admin_controller import router as admin_router
from .eventos.compras_controller import router as compras_router
from .ticktes.tickets_controller import router as tickets_router
from .usuarios.usuarios_controller import router as usuarios_router

app = FastAPI()
app.include_router(eventos_router)
app.include_router(admin_router)
app.include_router(compras_router)
app.include_router(tickets_router)
app.include_router(usuarios_router)

create_tables()

@app.get("/")
def root():
    return {"message": "API funcionando"}
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}