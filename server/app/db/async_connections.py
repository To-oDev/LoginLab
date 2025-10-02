import asyncpg

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/login_lab"

pool = None  # variable global del pool

async def init_db_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DATABASE_URL)
        print("Pool de conexiones inicializado.")

async def close_db_pool():
    global pool
    if pool:
        await pool.close()
        print("Pool de conexiones cerrado.")

# Context manager para obtener una conexión
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_connection():
    global pool
    if pool is None:
        raise RuntimeError("El pool no está inicializado")
    async with pool.acquire() as conn:
        yield conn
