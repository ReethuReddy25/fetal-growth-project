from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import users, admin, predict
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("who").setLevel(logging.INFO)

app = FastAPI(title="MidTrimester Growth")

# ✅ CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(predict.router, prefix="/api/predict", tags=["predict"])

#app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def index():
    return {"msg": "MidTrimester Growth API running. Visit /docs for API docs."}
