from .database import get_connection


def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # Una unica tabla de versionado (antes eran dos: user_profile_changes
    # y user_password_changes). Cada fila es un "snapshot" completo de
    # los campos mutables (name + password_hash) en el momento del
    # cambio. El campo que no cambio se copia igual, sin modificarse.
    # El estado vigente de un usuario es siempre la fila con mayor id
    # para ese user_id; si no hay ninguna, se usan los valores
    # originales de `users`. Ver usuarios_service.py.
    connection.execute("""
        CREATE TABLE IF NOT EXISTS user_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            changed_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()