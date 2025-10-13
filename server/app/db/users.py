from fastapi import HTTPException, status
from uuid import UUID
from passlib.hash import pbkdf2_sha256

from app.db.async_connections import get_connection

async def create_user(username: str, email: str, password: str):
    user = await get_user_by_username(username)
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
    async with get_connection() as conn:
        row = await conn.fetchrow(query, username, email, pbkdf2_sha256.hash(password))
        return row

async def delete_user_by_username(user_name: str):
    async with get_connection() as conn:
        user = await get_user_by_username(user_name)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return await conn.fetchrow("DELETE FROM users WHERE id = $1", user_name)

async def get_user_by_username(username: str):
    async with get_connection() as conn:
        query = "SELECT * FROM users WHERE username = $1"
        row = await conn.fetchrow(query, username)
        return row

async def get_users():
    async with get_connection() as conn:
        query = "SELECT * FROM users"
        rows = await conn.fetch(query)
        return rows
