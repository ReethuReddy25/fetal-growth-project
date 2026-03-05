import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal, engine, Base
from app.models import User
from app.security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()
email = "admin@example.com"
pwd = "AdminPass123"  # change after first login
exist = db.query(User).filter(User.email==email).first()
if exist:
    print("Admin exists:", email)
else:
    u = User(email=email, password_hash=hash_password(pwd), role="admin")
    db.add(u); db.commit()
    print("Created admin:", email, "password:", pwd)
db.close()
