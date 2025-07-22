from fastapi import APIRouter
from app.db.schema.user import UserInCreate, UserInLogin
authrouter = APIRouter()

@authrouter.post("/login")
def login(loginDetails: UserInLogin):
    return {"data":loginDetails}

@authrouter.post("/signup")
def signup(signUpDetails: UserInCreate):
    return {"data":signUpDetails}