from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import SessionLocal, Base, engine
from ..models import User
from ..schemas import UserCreate, UserOut
from ..security import hash_password, verify_password, create_access_token

router = APIRouter()

# Create tables if not already created
Base.metadata.create_all(bind=engine)


# ✅ Registration endpoint
@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate):
    db: Session = SessionLocal()
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Default role = "doctor"
    new_user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role="doctor"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ✅ Login endpoint
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    token = create_access_token(user.email, user.role)
    return {"access_token": token, "token_type": "bearer", "role": user.role}
