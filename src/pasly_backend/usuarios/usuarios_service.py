import sqlite3

from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..database.database import get_connection
from .usuarios_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def create_user(self, name: str, email: str, password: str, birth_date: str) -> User:
        password_hash = pwd_context.hash(password)

        connection = get_connection()
        try:
            cursor = connection.execute(
                "INSERT INTO users (name, email, password_hash, birth_date) VALUES (?, ?, ?, ?)",
                (name, email, password_hash, birth_date),
            )
            connection.commit()
            nuevo_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una cuenta registrada con ese email",
            )
        finally:
            connection.close()
        if nuevo_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el usuario",
            )
        return self.get_user(nuevo_id)

    def get_user(self, user_id: int) -> User:
        connection = get_connection()
        try:
            row = connection.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
        finally:
            connection.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return User.from_row(row)

    def list_users(self) -> list[User]:
        connection = get_connection()
        try:
            rows = connection.execute("SELECT * FROM users").fetchall()
        finally:
            connection.close()
        return [User.from_row(r) for r in rows]

    def authenticate(self, email: str, password: str) -> User:
        connection = get_connection()
        try:
            row = connection.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()
        finally:
            connection.close()

        credenciales_invalidas = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )

        if row is None:
            raise credenciales_invalidas

        usuario = self.get_user(row["id"])
        if not pwd_context.verify(password, usuario.password_hash):
            raise credenciales_invalidas

        return usuario