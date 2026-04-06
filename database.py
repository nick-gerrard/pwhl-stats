from settings import settings
from psycopg_pool import AsyncConnectionPool


pool: AsyncConnectionPool | None = None

async def get_pool() -> AsyncConnectionPool:
    return pool