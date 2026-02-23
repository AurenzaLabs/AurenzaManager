from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "AURENZA_SECRET"
ALGORITHM = "HS256"
# Prefer pbkdf2_sha256 for compatibility across local environments.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hash):
    try:
        return pwd_context.verify(password, hash)
    except Exception:
        # Treat unsupported/corrupt legacy hashes as invalid credentials.
        return False

def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + timedelta(hours=8)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
