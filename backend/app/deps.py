from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import decode_token
from .database import SessionLocal
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def get_current_doctor(user = Depends(get_current_user)):
    if user.role not in ("doctor", "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor access required")
    return user
