from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..guards.guards import obtener_usuario_autenticado, requiere_admin
from ..guards.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from .usuarios_dto import (
    AsignarRolRequest,
    LoginRequest,
    Token,
    UserCreate,
    UserResponse,
)
from .usuarios_model import User
from .usuarios_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

service = UserService()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(
        db,
        payload.name,
        payload.email,
        payload.password,
        payload.birth_date.strftime("%d-%m-%Y"),
    )

@router.get("/", response_model=list[UserResponse], dependencies=[Depends(requiere_admin)])
def list_users(db: Session = Depends(get_db)):
    return service.list_users(db)


# tokenUrl declarado en guards
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = service.authenticate(db, form_data.username, form_data.password)
    access_token = create_access_token(
        subject=str(usuario.id),
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


# Login via JSON
@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = service.authenticate(db, payload.email, payload.password)
    access_token = create_access_token(subject=str(usuario.id))
    return Token(access_token=access_token, token_type="bearer")


# Perfil del usuario autenticado
@router.get("/me", response_model=UserResponse)
def get_my_profile(usuario: User = Depends(obtener_usuario_autenticado)):
    return usuario

# asignar un nuevo rol a un usuario (solo admin)
@router.post("/{user_id}/rol", response_model=UserResponse, dependencies=[Depends(requiere_admin)])
def asignar_rol(user_id: int, payload: AsignarRolRequest, db: Session = Depends(get_db)):
    return service.asignar_rol(db, user_id, payload.rol)

# Consulta por id
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_user(db, user_id)