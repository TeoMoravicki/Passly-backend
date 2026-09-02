import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str
    password_hash: str
    birth_date: str
    created_at: str

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "User":
        return cls(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            birth_date=row["birth_date"],
            created_at=row["created_at"],
        )