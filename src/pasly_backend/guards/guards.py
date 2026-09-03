from fastapi import Depends, Header, HTTPException, status

from ..usuarios.usuarios_model import User
from ..usuarios.usuarios_service import UserService

service = UserService()


def obtener_usuario_autenticado(x_user_id: int = Header(..., alias="X-User-Id")) -> User:
    try:
        return service.get_user(x_user_id)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado o User-Id invalido",
        )


def requiere_rol(rol_requerido: str):

    def _verificar(usuario: User = Depends(obtener_usuario_autenticado)) -> User:
        if usuario.role != rol_requerido:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenes permisos suficientes para esta accion",
            )
        return usuario

    return _verificar


requiere_admin = requiere_rol("administrador")
