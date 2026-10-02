from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from pwdlib import PasswordHash

from fastapi import Response

from .config import settings


password_hash = PasswordHash.recommended()

ALGORITHM = "HS256"

COOKIE_NAME = "pocketsmart_token"


def hash_password(password: str) -> str:

    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed: str,
) -> bool:

    return password_hash.verify(
        password,
        hashed,
    )


def create_access_token(
    user_id: int,
) -> str:

    payload = {
        "sub": str(user_id),
        "exp": (
            datetime.now(timezone.utc)
            + timedelta(hours=12)
        ),
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> int | None:

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        return int(payload["sub"])

    except (
        JWTError,
        KeyError,
        TypeError,
        ValueError,
    ):

        return None


def set_auth_cookie(
    response: Response,
    user_id: int,
):

    token = create_access_token(
        user_id
    )

    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        secure=(
            settings.environment
            == "production"
        ),
        max_age=60 * 60 * 12,
    )


def clear_auth_cookie(
    response: Response,
):

    response.delete_cookie(
        COOKIE_NAME
    )