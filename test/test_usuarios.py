from datetime import timedelta

import jwt
import pytest
from fastapi import HTTPException

from conftest import SessionTest
from pasly_backend.guards import security
from pasly_backend.usuarios.usuarios_model import AsignacionRol
from pasly_backend.usuarios.usuarios_service import UserService, pwd_context

CLAVE = "clave12345"




def registrar(client, email="ana@mail.com", password=CLAVE):
    r = client.post(
        "/users/",
        json={"name": "Ana", "email": email, "password": password, "birth_date": "01-02-2000"},
    )
    assert r.status_code == 201
    return r.json()["id"]


def login(client, email="ana@mail.com", password=CLAVE):
    r = client.post("/users/login", json={"email": email, "password": password})
    assert r.status_code == 200
    return r.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def hacer_admin(user_id):
    with SessionTest() as db:
        db.add(AsignacionRol(user_id=user_id, rol="administrador"))
        db.commit()


# ---------- Unidad ----------

def test_password_se_guarda_hasheada_y_se_verifica():
    hash_ = pwd_context.hash(CLAVE)
    assert hash_ != CLAVE
    assert pwd_context.verify(CLAVE, hash_)
    assert not pwd_context.verify("otra", hash_)


def test_token_valido_contiene_sub_y_exp():
    payload = security.decode_access_token(security.create_access_token("5"))
    assert payload["sub"] == "5" and payload["exp"]


def test_token_vencido_es_rechazado():
    token = security.create_access_token("5", expires_delta=timedelta(seconds=-1))
    with pytest.raises(jwt.ExpiredSignatureError):
        security.decode_access_token(token)


def test_token_con_firma_invalida_es_rechazado():
    falso = jwt.encode({"sub": "5", "exp": 9999999999}, "otra-clave", algorithm="HS256")
    with pytest.raises(jwt.InvalidTokenError):
        security.decode_access_token(falso)


def test_rol_vigente_es_la_ultima_asignacion(client):
    user_id = registrar(client)
    service = UserService()
    with SessionTest() as db:
        assert service.obtener_rol_actual(db, user_id) == "usuario"
        service.asignar_rol(db, user_id, "administrador")
        service.asignar_rol(db, user_id, "usuario")
        assert service.obtener_rol_actual(db, user_id) == "usuario"


def test_token_de_reset_es_de_un_solo_uso(client):
    registrar(client)
    service = UserService()
    with SessionTest() as db:
        token = service.solicitar_reset_password(db, "ana@mail.com")
        assert token is not None
        service.resetear_password(db, token, "nueva-clave-1")
        with pytest.raises(HTTPException) as error:
            service.resetear_password(db, token, "otra-clave-22")
        assert error.value.status_code == 400


# ---------- API: registro y login ----------

def test_registro_ok_no_expone_el_hash(client):
    r = client.post(
        "/users/",
        json={"name": "Ana", "email": "ana@mail.com", "password": CLAVE, "birth_date": "01-02-2000"},
    )
    assert r.status_code == 201
    assert "password_hash" not in r.json() and "password" not in r.json()


def test_registro_con_email_duplicado_da_409(client):
    registrar(client)
    r = client.post(
        "/users/",
        json={"name": "Ana", "email": "ana@mail.com", "password": CLAVE, "birth_date": "01-02-2000"},
    )
    assert r.status_code == 409


def test_registro_con_password_corta_da_422(client):
    r = client.post(
        "/users/",
        json={"name": "Ana", "email": "ana@mail.com", "password": "corta", "birth_date": "01-02-2000"},
    )
    assert r.status_code == 422


def test_login_con_password_incorrecta_da_401(client):
    registrar(client)
    r = client.post("/users/login", json={"email": "ana@mail.com", "password": "incorrecta1"})
    assert r.status_code == 401


def test_login_con_email_inexistente_da_401(client):
    r = client.post("/users/login", json={"email": "nadie@mail.com", "password": CLAVE})
    assert r.status_code == 401


# ---------- API: 401 ----------

def test_me_sin_token_da_401(client):
    assert client.get("/users/me").status_code == 401


def test_me_con_token_invalido_da_401(client):
    assert client.get("/users/me", headers=auth("no-es-un-jwt")).status_code == 401


def test_me_con_token_vencido_da_401(client):
    user_id = registrar(client)
    vencido = security.create_access_token(str(user_id), expires_delta=timedelta(seconds=-1))
    assert client.get("/users/me", headers=auth(vencido)).status_code == 401


def test_me_con_token_valido_da_200(client):
    registrar(client)
    r = client.get("/users/me", headers=auth(login(client)))
    assert r.status_code == 200 and r.json()["email"] == "ana@mail.com"


def test_logout_revoca_el_token(client):
    registrar(client)
    token = login(client)
    assert client.post("/users/logout", headers=auth(token)).status_code == 204
    assert client.get("/users/me", headers=auth(token)).status_code == 401


# ---------- API: 403 ----------

def test_listar_usuarios_sin_token_da_401(client):
    assert client.get("/users/").status_code == 401


def test_listar_usuarios_siendo_usuario_comun_da_403(client):
    registrar(client)
    assert client.get("/users/", headers=auth(login(client))).status_code == 403


def test_listar_usuarios_siendo_admin_da_200(client):
    admin_id = registrar(client, "admin@mail.com")
    hacer_admin(admin_id)
    r = client.get("/users/", headers=auth(login(client, "admin@mail.com")))
    assert r.status_code == 200


def test_asignar_rol_sin_token_da_401(client):
    user_id = registrar(client)
    assert client.post(f"/users/{user_id}/rol", json={"rol": "administrador"}).status_code == 401


def test_asignar_rol_siendo_usuario_comun_da_403(client):
    user_id = registrar(client)
    r = client.post(f"/users/{user_id}/rol", json={"rol": "administrador"}, headers=auth(login(client)))
    assert r.status_code == 403


def test_asignar_rol_siendo_admin_da_200_y_el_rol_vigente_cambia(client):
    admin_id = registrar(client, "admin@mail.com")
    hacer_admin(admin_id)
    user_id = registrar(client)
    r = client.post(
        f"/users/{user_id}/rol", json={"rol": "administrador"}, headers=auth(login(client, "admin@mail.com"))
    )
    assert r.status_code == 200 and r.json()["role"] == "administrador"
    # el usuario ascendido ya puede listar usuarios, sin volver a iniciar sesion
    assert client.get("/users/", headers=auth(login(client))).status_code == 200


def test_asignar_rol_invalido_da_422(client):
    admin_id = registrar(client, "admin@mail.com")
    hacer_admin(admin_id)
    r = client.post(
        f"/users/{admin_id}/rol", json={"rol": "superuser"}, headers=auth(login(client, "admin@mail.com"))
    )
    assert r.status_code == 422


# ---------- API: recuperacion de contraseña ----------

def test_forgot_password_no_revela_si_el_email_existe(client):
    registrar(client)
    existente = client.post("/users/forgot-password", json={"email": "ana@mail.com"}).json()
    inexistente = client.post("/users/forgot-password", json={"email": "nadie@mail.com"}).json()
    assert existente["detail"] == inexistente["detail"]
    assert inexistente["reset_token"] is None


def test_reset_password_cambia_la_clave_y_el_token_no_se_reusa(client):
    registrar(client)
    token = client.post("/users/forgot-password", json={"email": "ana@mail.com"}).json()["reset_token"]
    assert client.post("/users/reset-password", json={"token": token, "new_password": "nueva-clave-1"}).status_code == 204
    assert client.post("/users/login", json={"email": "ana@mail.com", "password": "nueva-clave-1"}).status_code == 200
    assert client.post("/users/login", json={"email": "ana@mail.com", "password": CLAVE}).status_code == 401
    r = client.post("/users/reset-password", json={"token": token, "new_password": "otra-clave-22"})
    assert r.status_code == 400


# ---------- Logs ----------

def test_los_eventos_de_auth_se_registran(client, caplog):
    with caplog.at_level("INFO", logger="passly"):
        registrar(client)
        token = login(client)
        client.post("/users/login", json={"email": "ana@mail.com", "password": "incorrecta1"})
        client.get("/users/me", headers=auth("no-es-un-jwt"))
        client.post("/users/logout", headers=auth(token))
    texto = caplog.text
    for evento in ("usuario registrado", "login exitoso", "login fallido", "token invalido", "logout"):
        assert evento in texto


def test_los_logs_no_contienen_tokens_ni_passwords(client, caplog):
    registrar(client)
    with caplog.at_level("INFO", logger="passly"):
        token = login(client)
        client.get("/users/me", headers=auth(token))
        client.post("/users/login", json={"email": "ana@mail.com", "password": "incorrecta1"})
        client.post("/users/logout", headers=auth(token))
    assert token not in caplog.text
    assert CLAVE not in caplog.text and "incorrecta1" not in caplog.text
