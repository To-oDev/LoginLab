from datetime import datetime, timedelta
from jose import jwt
from app.db.async_connections import get_connection
from uuid import UUID

SECRET_KEY = "TU_SECRET_KEY_AQUI"  # cambiar por una variable de entorno
ALGORITHM = "HS256"

async def create_access_token(user_id: str, expires_delta: timedelta):
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

async def get_tokens():
    async with get_connection() as conn:
        return await conn.fetch("SELECT * FROM tokens")
        
async def user_has_token(user_id: str):
    async with get_connection() as conn:
        return await conn.fetchrow("SELECT * FROM tokens WHERE user_id = $1", user_id)