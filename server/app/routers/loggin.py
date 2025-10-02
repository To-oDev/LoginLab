from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta, datetime
from app.db.async_connections import get_connection
from app.db.users import get_user_by_username
from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    # Obtenemos la conexión de manera segura
    async with get_connection() as conn:
        user = await get_user_by_username(request.username, conn)
        if not user or not pwd_context.verify(request.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Ajustar expiración según remember_me
    expire_minutes = (
        ACCESS_TOKEN_REMEMBER_ME_MINUTES if request.remember_me else ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token_expires = timedelta(minutes=expire_minutes)
    access_token = await create_access_token(user["id"], access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

SECRET_KEY = "TU_SECRET_KEY_AQUI"  # cambiar por una variable de entorno
ALGORITHM = "HS256"
async def create_access_token(user_id: str, expires_delta: timedelta):
    """
    Crea un token JWT y lo guarda en la tabla 'tokens'.
    :param user_id: UUID del usuario
    :param expires_delta: timedelta hasta expiración
    :return: token string
    """
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(user_id),
        "exp": expire.timestamp()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Guardar token en DB
    async with get_connection() as conn:
        await conn.execute(
            """
            INSERT INTO tokens (user_id, token, expires_at)
            VALUES ($1, $2, $3)
            """,
            user_id,
            token,
            expire
        )

    return token
