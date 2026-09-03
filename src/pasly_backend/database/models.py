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
            role TEXT NOT NULL CHECK (role IN ('usuario', 'administrador')),
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    connection.commit()
    connection.close()