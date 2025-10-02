from fastapi import HTTPException, status
from passlib.context import CryptContext
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(username: str, email: str, password: str, conn):
    user = await get_user_by_username(username, conn)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario o email ya existe"
        )

    # hashed_password = pwd_context.hash(password[:72])
    query = """
        INSERT INTO users (username, email, hashed_password)
        VALUES ($1, $2, $3)
        RETURNING id, username, email
    """
    row = await conn.fetchrow(query, username, email, password)
    return row

async def delete_user(user_id: UUID, conn):
    user = await get_user_by_username(user_id, conn)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await conn.fetchrow("DELETE FROM users WHERE id = $1", str(user_id))

async def get_user_by_username(username: str, conn):
    query = "SELECT * FROM users WHERE username = $1"
    row = await conn.fetchrow(query, username)
    return row
