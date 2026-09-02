from fastapi import APIRouter, Depends, Header, HTTPException, status

from .usuarios_dto import LoginRequest, UserCreate, UserResponse
from .usuarios_model import User
from .usuarios_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

service = UserService()


def obtener_usuario_autenticado(x_user_id: int = Header(..., alias="X-User-Id")) -> User:
    try:
        return service.get_user(x_user_id)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado o X-User-Id invalido",
        )


# Alta y consulta

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate):
    return service.create_user(
        payload.name, payload.email, payload.password, payload.birth_date.isoformat()
    )

@router.get("/", response_model=list[UserResponse])
def list_users():
    return service.list_users()


# Login

@router.post("/login", response_model=UserResponse)
def login(payload: LoginRequest):
    return service.authenticate(payload.email, payload.password)


# Perfil del usuario autenticado

@router.get("/me", response_model=UserResponse)
def get_my_profile(usuario: User = Depends(obtener_usuario_autenticado)):
    return usuario


# Consulta por id
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return service.get_user(user_id)