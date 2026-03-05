import os
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

SECRET = os.getenv("SECRET_KEY", "change-this-secret")
ALGO = "HS256"
ACCESS_EXPIRE_HOURS = 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_access_token(email: str, role: str):
    expire = datetime.utcnow() + timedelta(hours=ACCESS_EXPIRE_HOURS)
    payload = {"sub": email, "role": role, "exp": expire.isoformat()}
    token = jwt.encode(payload, SECRET, algorithm=ALGO)
    return token

def decode_token(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return data
    except Exception:
        return None
