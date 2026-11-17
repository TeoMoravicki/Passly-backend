def test_crear_y_consultar_evento(client):
    datos = {
        "nombre": "Festival de Rock",
        "descripcion": "Evento de prueba",
        "capacidad_maxima": 500,
        "lugar": "Posadas",
        "precio_base": 20000,
        "estado": "ACTIVO",
        "imagen": "festival.jpg"
    }

    respuesta = client.post("/eventos/", json=datos)

    assert respuesta.status_code == 200

    evento_id = respuesta.json()["id"]

    consulta = client.get(f"/eventos/{evento_id}")

    assert consulta.status_code == 200
    assert consulta.json()["nombre"] == "Festival de Rock"


def test_listar_eventos(client):
    datos = {
        "nombre": "Concierto",
        "descripcion": "Concierto de prueba",
        "capacidad_maxima": 300,
        "lugar": "Obera",
        "precio_base": 15000,
        "estado": "ACTIVO",
        "imagen": "concierto.jpg"
    }

    client.post("/eventos/", json=datos)

    respuesta = client.get("/eventos/")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) >= 1
    assert respuesta.json()[0]["nombre"] == "Concierto"