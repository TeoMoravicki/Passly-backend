def test_crear_categoria(client):
    datos = {
        "nombre": "VIP",
        "precio": 30000,
        "lugar": "Sector A"
    }

    respuesta = client.post("/categoria/", json=datos)

    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "VIP"
    assert respuesta.json()["precio"] == 30000
    assert respuesta.json()["lugar"] == "Sector A"


def test_consultar_categoria(client):
    datos = {
        "nombre": "General",
        "precio": 15000,
        "lugar": "Campo"
    }

    creacion = client.post("/categoria/", json=datos)

    assert creacion.status_code == 200

    categoria_id = creacion.json()["id"]

    respuesta = client.get(f"/categoria/{categoria_id}")

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == categoria_id
    assert respuesta.json()["nombre"] == "General"


def test_listar_categorias(client):
    datos = {
        "nombre": "Platea",
        "precio": 25000,
        "lugar": "Sector B"
    }

    creacion = client.post("/categoria/", json=datos)

    assert creacion.status_code == 200

    categoria_id = creacion.json()["id"]

    respuesta = client.get("/categoria/")

    assert respuesta.status_code == 200
    assert any(
        categoria["id"] == categoria_id
        for categoria in respuesta.json()
    )