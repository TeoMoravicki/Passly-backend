import sqlite3

from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..database.database import get_connection
from .usuarios_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    # Alta 
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
                        detail="Error al generar el identificador del usuario",
                    )
        return self.get_user(nuevo_id)

    # Lectura
    def get_user(self, user_id: int) -> User:
        connection = get_connection()
        try:
            row = connection.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            name, password_hash = self._estado_vigente(
                connection, user_id, row["name"], row["password_hash"]
            )
        finally:
            connection.close()

        return User(
            id=row["id"],
            name=name,
            email=row["email"],
            password_hash=password_hash,
            birth_date=row["birth_date"],
            created_at=row["created_at"],
        )

    def list_users(self) -> list[User]:
        connection = get_connection()
        try:
            rows = connection.execute("SELECT * FROM users").fetchall()
            usuarios = []
            for row in rows:
                name, password_hash = self._estado_vigente(
                    connection, row["id"], row["name"], row["password_hash"]
                )
                usuarios.append(
                    User(
                        id=row["id"],
                        name=name,
                        email=row["email"],
                        password_hash=password_hash,
                        birth_date=row["birth_date"],
                        created_at=row["created_at"],
                    )
                )
        finally:
            connection.close()
        return usuarios


    # Login (autenticacion)
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

    
    # Actualizar perfil
    
    def update_name(self, user_id: int, new_name: str) -> User:
        usuario_actual = self.get_user(user_id)  # valida que exista (404 si no)

        connection = get_connection()
        try:
            connection.execute(
                "INSERT INTO user_updates (user_id, name, password_hash) VALUES (?, ?, ?)",
                (user_id, new_name, usuario_actual.password_hash),
            )
            connection.commit()
        finally:
            connection.close()

        return self.get_user(user_id)

    # Cambiar contraseña

    def change_password(self, user_id: int, current_password: str, new_password: str) -> None:
        usuario_actual = self.get_user(user_id)

        if not pwd_context.verify(current_password, usuario_actual.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="La contraseña actual no es correcta",
            )

        nuevo_hash = pwd_context.hash(new_password)
        connection = get_connection()
        try:
            connection.execute(
                "INSERT INTO user_updates (user_id, name, password_hash) VALUES (?, ?, ?)",
                (user_id, usuario_actual.name, nuevo_hash),
            )
            connection.commit()
        finally:
            connection.close()


    #resuelve name + password_hash vigentes
    def _estado_vigente(
        self, connection, user_id: int, name_original: str, hash_original: str
    ) -> tuple[str, str]:
        row = connection.execute(
            "SELECT name, password_hash FROM user_updates WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        if row is None:
            return name_original, hash_original
        return row["name"], row["password_hash"]
