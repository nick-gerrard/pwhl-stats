from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg_pool import AsyncConnectionPool

import database
from routers import games, players, standings, stats, teams
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.pool = AsyncConnectionPool(conninfo=settings.database_url, open=False)
    await database.pool.open()
    yield
    await database.pool.close()
    # Shutdown Code


app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["GET"])

app.include_router(teams.router)
app.include_router(players.router)
app.include_router(stats.router)
app.include_router(standings.router)
app.include_router(games.router)


@app.get("/")
def root():
    return {"status": "ok"}
