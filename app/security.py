from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.config import settings

password_hash = PasswordHash.recommended()  # argon2 z zalecanymi parametrami


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


class TokenError(Exception):
    """Token nieprawidłowy: zły podpis, wygasły, uszkodzony."""


def create_access_token(partner_id: int) -> tuple[str, datetime]:
    now = datetime.now(UTC)
    expires_at = now + timedelta(hours=settings.jwt_expire_hours)
    payload = {"sub": str(partner_id), "iat": now, "exp": expires_at}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, expires_at


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["exp", "sub"]},
        )
        return int(payload["sub"])
    except (jwt.InvalidTokenError, ValueError) as exc:
        raise TokenError() from exc
