from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

Rol = Literal["usuario", "administrador"]


class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=8)
    birth_date: date


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    birth_date: date
    role: Rol
    created_at: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
