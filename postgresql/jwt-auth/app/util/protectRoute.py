from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.service.userService import UserService
from app.core.database import get_db
from app.db.schema.user import UserOutput

AUTH_PREFIX = 'Bearer '

def get_current_user(
    session: Session = Depends(get_db),
    authorization: Annotated[Union[str, None], Header()] = None
) -> UserOutput:
    print("Incoming Authorization:", authorization)

    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if not authorization:
        print("No authorization header found.")
        raise auth_exception

    if not authorization.startswith(AUTH_PREFIX):
        print("Authorization header doesn't start with 'Bearer '.")
        raise auth_exception

    token = authorization[len(AUTH_PREFIX):].strip()
    print("Token extracted:", token)

    payload = AuthHandler.decode_jwt(token)
    print("Decoded payload:", payload)

    if not payload or not payload.get("user_id"):
        print("Invalid payload or missing user_id")
        raise auth_exception

    user = UserService(session=session).get_user_by_id(payload["user_id"])
    print("User fetched from DB:", user)

    if not user:
        print("User not found in DB.")
        raise auth_exception

    return UserOutput(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )
