from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import users, admin, predict
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="MidTrimester Growth")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Templates ----------------
templates = Jinja2Templates(directory="app/templates")

# ---------------- Routers ----------------
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(predict.router, prefix="/api/predict", tags=["predict"])


# ---------------- Frontend Path ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
print("FRONTEND_DIR:", FRONTEND_DIR)

# serve frontend static files
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


# ---------------- Home Page ----------------
@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))


# ---------------- Health Check ----------------
@app.get("/health")
def health():
    return {"status": "API running"}