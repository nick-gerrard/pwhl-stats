from contextlib import asynccontextmanager
from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool
from settings import settings
import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.pool = AsyncConnectionPool(conninfo=settings.database_url, open=False)
    await database.pool.open()
    yield
    await database.pool.close()
    # Shutdown Code

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"status": "ok"}