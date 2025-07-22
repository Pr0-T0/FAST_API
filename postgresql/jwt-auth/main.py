from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authrouter

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