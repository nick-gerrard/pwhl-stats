import asyncio
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg_pool import AsyncConnectionPool

import database
from ingestions.run import run_all
from routers import games, players, standings, stats, teams
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.pool = AsyncConnectionPool(conninfo=settings.database_url, open=False)
    await database.pool.open()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_all, CronTrigger(hour=4, minute=0))
    scheduler.start()
    yield
    scheduler.shutdown()
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


@app.post("/admin/ingest")
async def trigger_ingestion(x_admin_token: str = Header(...)):
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=403)
    asyncio.create_task(run_all())
    return {"status": "ingestion started"}
