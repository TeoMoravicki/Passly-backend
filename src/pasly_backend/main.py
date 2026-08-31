from fastapi import FastAPI
from .eventos.eventos_controller import router as eventos_router

app = FastAPI()


app.include_router(eventos_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}