from db.async_connections import get_connection
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------
# Búsqueda
# -------------------------
def get_user_by_username(username: str):
    query = "SELECT * FROM users WHERE username = %s"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (username,))
            return cursor.fetchone()

# -------------------------
# Búsqueda
# -------------------------
async def get_user_by_username_async(username: str):
    query = "SELECT * FROM users WHERE username = $1"
    async with get_connection() as conn:
        row = await conn.fetchrow(query, username)
        return row


# -------------------------
# Registro
# -------------------------
def create_user(username: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    query = """
        INSERT INTO users (username, email, hashed_password)
        VALUES (%s, %s, %s)
        RETURNING id, username, email, created_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (username, email, hashed_password))
            conn.commit()
            return cursor.fetchone()

# -------------------------
# Eliminación
# -------------------------
def delete_user(username: str):
    query = "DELETE FROM users WHERE username = %s RETURNING id, username"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (username,))
            conn.commit()
            return cursor.fetchone()

# -------------------------
# Login / Autenticación
# -------------------------
def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if user and pwd_context.verify(password, user[3]):  # hashed_password está en la posición 3
        return user
    return None
