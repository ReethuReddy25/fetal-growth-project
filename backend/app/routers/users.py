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


# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Registration endpoint
@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):

    # 🔥 Normalize email (VERY IMPORTANT)
    email = user_in.email.strip().lower()

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        email=email,
        password_hash=hash_password(user_in.password),
        role="doctor"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ✅ Login endpoint
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # 🔥 Normalize email
    email = form_data.username.strip().lower()

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    token = create_access_token(user.email, user.role)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }