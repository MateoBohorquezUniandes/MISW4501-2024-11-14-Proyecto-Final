import bcrypt


def set_password(password: str) -> str:
    """Hash a password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(hashed_password: str, password: str) -> bool:
    """Check a password against the hashed version."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
