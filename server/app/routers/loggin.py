# Router for log in
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, constr
from datetime import datetime, timedelta
from app.db.async_connections import get_connection
from passlib.context import CryptContext
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_REMEMBER_ME_MINUTES = 60 * 24 * 7  # 7 días

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo Pydantic
class LoginRequest(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6)
    remember_me: bool = False  # <-- checkbox

class Token(BaseModel):
    access_token: str
    token_type: str

# Funciones helpers
async def verify_user_password(username: str, password: str):
    query = "SELECT username, hashed_password FROM users WHERE username = $1"
    async with get_connection() as conn:
        row = await conn.fetchrow(query, username)
        if row and pwd_context.verify(password, row["hashed_password"]):
            return {"username": row["username"]}
    return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

router = APIRouter()

# Endpoint login
@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    user = await verify_user_password(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ajustar expiración según remember_me
    if request.remember_me:
        expire_minutes = ACCESS_TOKEN_REMEMBER_ME_MINUTES
    else:
        expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    access_token_expires = timedelta(minutes=expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
