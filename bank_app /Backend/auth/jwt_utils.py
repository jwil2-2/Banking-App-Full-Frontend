# Creates and verifies short-lived JWT access tokens.
# JWT_SECRET_KEY is required; JWT_ACCESS_TOKEN_MINUTES defaults to 60.
# Authorization uses the current MongoDB user rather than trusting token roles.

import os
from datetime import datetime, timedelta, timezone

import jwt

ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_MINUTES", "60"))


def _secret_key() -> str:
    # Return the signing secret and fail fast when it is not configured.
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise RuntimeError("JWT_SECRET_KEY is not set")
    return secret


def create_access_token(*, user_id: str, role: str, email: str) -> str:
    # Create a signed token containing subject, role, email, and UTC expiry.
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    payload = {
        "sub": user_id,
        "role": role,
        "email": email,
        "exp": expires,
    }
    return jwt.encode(payload, _secret_key(), algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    # Verify the token signature and expiry before returning its claims.
    return jwt.decode(token, _secret_key(), algorithms=[ALGORITHM])
