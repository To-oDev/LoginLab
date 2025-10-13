from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta
from app.db.users import get_user_by_username
from passlib.hash import pbkdf2_sha256
from app.db.tokens import create_access_token, user_has_token

class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: bool

class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_REMEMBER_ME_MINUTES = 60*24*7  # 7 días

@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    user = await get_user_by_username(request.username)
    if not user or not pbkdf2_sha256.verify(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = await user_has_token(user["id"])
    if not token:
        # Ajustar expiración según remember_me
        expire_minutes = (
            ACCESS_TOKEN_REMEMBER_ME_MINUTES if request.remember_me else ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token_expires = timedelta(minutes=expire_minutes)
        access_token = await create_access_token(user["id"], access_token_expires)
        return Token(access_token=access_token, token_type="bearer")

    return Token(access_token=token["token"], token_type="bearer")


