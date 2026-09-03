from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, BeforeValidator, PlainSerializer
from typing_extensions import Annotated

# 1. Función para convertir el texto de entrada 'dd-mm-yyyy' a un objeto date de Python
def parse_custom_date(v: any) -> date:
    if isinstance(v, str):
        return datetime.strptime(v, "%d-%m-%Y").date()
    return v

# 2. Tipo de dato personalizado que valida la entrada Y formatea la salida en formato dd-mm-yyyy
CustomDate = Annotated[
    date,
    BeforeValidator(parse_custom_date),
    PlainSerializer(lambda v: v.strftime("%d-%m-%Y"), return_type=str)
]


class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=8)
    birth_date: CustomDate


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    birth_date: CustomDate
    role: str
    created_at: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str