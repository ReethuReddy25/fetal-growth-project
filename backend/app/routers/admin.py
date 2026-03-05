from fastapi import APIRouter, Depends, HTTPException
from ..schemas import UserCreate
from ..database import SessionLocal
from ..models import User
from ..security import hash_password
from ..deps import get_current_doctor
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create-doctor")
def create_doctor(payload: UserCreate, current_user=Depends(get_current_doctor)):
    # Only admin can create doctor accounts
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    db: Session = SessionLocal()
    exist = db.query(User).filter(User.email==payload.email).first()
    if exist:
        raise HTTPException(status_code=400, detail="User exists")
    user = User(email=payload.email, password_hash=hash_password(payload.password), role="doctor")
    db.add(user); db.commit(); db.refresh(user)
    return {"msg": "Doctor created", "email": user.email}
