def test_app_arranca(client):
    respuesta = client.get("/")

    assert respuesta.status_code == 200