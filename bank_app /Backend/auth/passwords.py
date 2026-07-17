# Password hashing and verification helpers.

import bcrypt


def hash_password(password: str) -> str:
    # Hash a UTF-8 password with a bcrypt-generated salt.
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, stored_password: str) -> bool:
    # Verify against bcrypt or a legacy plaintext value.
    # Remove the plaintext fallback after all old records migrate to bcrypt.
    if stored_password.startswith("$2"):
        return bcrypt.checkpw(plain_password.encode("utf-8"), stored_password.encode("utf-8"))
    return plain_password == stored_password
