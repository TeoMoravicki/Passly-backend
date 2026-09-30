from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from ..database.database import get_db
from ..usuarios.usuarios_model import User
from ..usuarios.usuarios_service import UserService
from .security import decode_access_token

service = UserService()

# tokenUrl es el endpoint que emite el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def obtener_usuario_autenticado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token expiro, vuelva a iniciar sesion",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credenciales_invalidas

    user_id = payload.get("sub")
    if user_id is None:
        raise credenciales_invalidas

    try:
        return service.get_user(db, int(user_id))
    except (HTTPException, ValueError):
        raise credenciales_invalidas


def requiere_rol(rol_requerido: str):

    def _verificar(usuario: User = Depends(obtener_usuario_autenticado)) -> User:
        if usuario.role != rol_requerido:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes para esta accion",
            )
        return usuario

    return _verificar

requiere_admin = requiere_rol("administrador")