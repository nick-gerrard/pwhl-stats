from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection

from database import get_conn, get_current_season
from queries.stats import get_goalie_info, get_goalie_stats, get_player_info, get_skater_stats
from schemas import GoalieInfo, GoalieStats, PlayerInfo, SkaterStats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/skaters", response_model=list[SkaterStats])
async def skater_stats(season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id, _ = await get_current_season(conn)
    return await get_skater_stats(conn, season_id)


@router.get("/skaters/{player_id}", response_model=PlayerInfo)
async def player_info(player_id: int, season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id, _ = await get_current_season(conn)
    result = await get_player_info(conn, season_id, player_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return result


@router.get("/goalies", response_model=list[GoalieStats])
async def goalie_stats(season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id, _ = await get_current_season(conn)
    return await get_goalie_stats(conn, season_id)


@router.get("/goalies/{player_id}", response_model=GoalieInfo)
async def goalie_info(player_id: int, season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id, _ = await get_current_season(conn)
    result = await get_goalie_info(conn, season_id, player_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Goalie not found")
    return result
