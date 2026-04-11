import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg_pool import AsyncConnectionPool

import database
from ingestions.run import run_all
from live.poller import check_start_time, get_today_game_ids, polling_loop
from routers import games, live, players, playoffs, seasons, standings, stats, teams
from settings import settings


async def schedule_polling(scheduler: AsyncIOScheduler) -> None:
    assert database.pool is not None
    async with database.pool.connection() as conn:
        result = await check_start_time(conn)
        expected_ids = await get_today_game_ids(conn)

    if settings.enable_polling and result and result["start_time"] and expected_ids:
        if result["start_time"] <= datetime.now(timezone.utc):
            asyncio.create_task(polling_loop(expected_ids))
        else:
            scheduler.add_job(
                polling_loop,
                DateTrigger(run_date=result["start_time"]),
                args=[expected_ids],
            )


async def run_all_and_reschedule(scheduler: AsyncIOScheduler) -> None:
    await run_all()
    await schedule_polling(scheduler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.pool = AsyncConnectionPool(conninfo=settings.database_url, open=False)
    await database.pool.open()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_all_and_reschedule,
        CronTrigger(hour=4, minute=0),
        args=[scheduler],
    )
    scheduler.start()

    await schedule_polling(scheduler)

    yield
    scheduler.shutdown()
    await database.pool.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://pwhl.nickgerrard.dev"],
    allow_methods=["GET", "POST"],
)

app.include_router(teams.router)
app.include_router(players.router)
app.include_router(stats.router)
app.include_router(standings.router)
app.include_router(games.router)
app.include_router(playoffs.router)
app.include_router(seasons.router)
app.include_router(live.router)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/admin/ingest")
async def trigger_ingestion(x_admin_token: str = Header(...)):
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=403)
    asyncio.create_task(run_all())
    return {"status": "ingestion started"}
