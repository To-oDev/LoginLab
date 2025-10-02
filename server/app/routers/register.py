from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, constr
from passlib.context import CryptContext
from app.db.async_connections import get_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tiempo de expiración por defecto del JWT (si decides crear token al registrar)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Modelo Pydantic
class RegisterRequest(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6)
    accept_terms: bool

# Modelo de respuesta simplificado
class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str

# Función helper para crear usuario
async def create_user(username: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    query = """
        INSERT INTO users (username, email, hashed_password)
        VALUES ($1, $2, $3)
        RETURNING id, username, email
    """
    async with get_connection() as conn:
        row = await conn.fetchrow(query, username, email, hashed_password)
        return row

# Endpoint de registro
@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    # Validar que el usuario aceptó los términos
    if not request.accept_terms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes aceptar los términos y condiciones"
        )

    # Verificar que no exista username o email duplicado
    async with get_connection() as conn:
        existing = await conn.fetchrow(
            "SELECT 1 FROM users WHERE username=$1 OR email=$2",
            request.username, request.email
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario o email ya existe"
            )

    # Crear usuario
    user = await create_user(request.username, request.email, request.password)
    return user
