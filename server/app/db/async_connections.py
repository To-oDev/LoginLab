# Configuración de conexión asíncrona
import asyncpg
from contextlib import asynccontextmanager

# Configuración de conexión vía variable de entorno
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/person_gpt"

# Crear pool de conexiones
pool: asyncpg.pool.Pool | None = None

# Función asíncrona para crear el pool
async def init_db_pool():
    global pool
    pool = await asyncpg.create_pool(
        dsn=DATABASE_URL,
        min_size=1,
        max_size=20
    )
    print("✅ Async pool creado")

# Función asiatcrona para cerrar el pool
async def close_db_pool():
    global pool
    if pool:
        await pool.close()
        print("✅ Pool cerrado")

# Context manager para usar la conexión de manera segura
@asynccontextmanager
async def get_connection():
    if pool is None:
        raise RuntimeError("El pool no está inicializado")
    async with pool.acquire() as conn:
        yield conn
