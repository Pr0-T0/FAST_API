from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authrouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import UserOutput

@asynccontextmanager
async def lifespan(app : FastAPI):
    #db startup initialization
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=authrouter, tags=["auth"], prefix="/auth")

@app.get("/health")
def health_check():
    return {"status" : "Running..."}

@app.get("/protected")
def read_protected(user : UserOutput = Depends(get_current_user)):
    return {"data": user}