from fastapi import FastAPI

from .database.models import create_tables
#from .database.create_admin import create_admin_user
from .eventos.eventos_controller import router as eventos_router
from .usuarios.usuarios_controller import router as usuarios_router

app = FastAPI()


app.include_router(eventos_router)
app.include_router(usuarios_router)

create_tables()
#init_db()

@app.get("/")
def root():
    return {"message": "API funcionando"}