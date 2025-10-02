from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, constr
from app.db.async_connections import get_connection
from app.db.users import create_user
from uuid import UUID

router = APIRouter()

# -------------------------
# Modelos Pydantic
# -------------------------
class RegisterRequest(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6, max_length=50)
    accept_terms: bool

class RegisterResponse(BaseModel):
    id: UUID
    username: str
    email: str

# -------------------------
# Endpoint de registro
# -------------------------
@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    # Obtenemos la conexión de manera segura
    async with get_connection() as conn:
        # Validar que el usuario aceptó los términos
        if not request.accept_terms:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debes aceptar los términos y condiciones"
            )

        # Crear usuario
        user = await create_user(request.username, request.email, request.password, conn)
        print("User:", user)
    return RegisterResponse(id=user["id"], username=user["username"], email=user["email"])