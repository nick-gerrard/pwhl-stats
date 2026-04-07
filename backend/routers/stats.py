from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn, get_current_season
from queries.stats import get_goalie_stats, get_skater_stats
from schemas import GoalieStats, SkaterStats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/skaters", response_model=list[SkaterStats])
async def skater_stats(conn: AsyncConnection = Depends(get_conn)):
    season_id, _ = await get_current_season(conn)
    return await get_skater_stats(conn, season_id)


@router.get("/goalies", response_model=list[GoalieStats])
async def goalie_stats(conn: AsyncConnection = Depends(get_conn)):
    season_id, _ = await get_current_season(conn)
    return await get_goalie_stats(conn, season_id)
