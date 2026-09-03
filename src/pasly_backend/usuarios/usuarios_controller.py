from fastapi import APIRouter, Depends

from ..guards.guards import obtener_usuario_autenticado, requiere_admin
from .usuarios_dto import LoginRequest, UserCreate, UserResponse
from .usuarios_model import User
from .usuarios_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

service = UserService()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate):
    return service.create_user(
        payload.name,
        payload.email,
        payload.password,
        payload.birth_date.isoformat(),
    )

@router.get("/", response_model=list[UserResponse])
def list_users(usuario: User = Depends(requiere_admin)):
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