import os
from datetime import datetime, timedelta, timezone

import jwt
from .redis_client import blacklist_token, is_token_blacklisted

SECRET_KEY = os.environ.get("PASSLY_JWT_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("PASSLY_JWT_EXPIRE_MINUTES", "30"))

#Genera un JWT
def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decodifica y valida firma/expiracion
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def revoke_access_token(token: str) -> None:
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        return

    exp = payload.get("exp")
    if exp is None:
        return

    ttl_seconds = int(exp - datetime.now(timezone.utc).timestamp())
    blacklist_token(token, ttl_seconds)

def token_esta_revocado(token: str) -> bool:
    return is_token_blacklisted(token)