from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection

from database import get_conn, get_current_season, get_current_regular_season_id
from queries.stats import (
    get_goalie_career,
    get_goalie_info,
    get_goalie_leaders,
    get_goalie_stats,
    get_player_career,
    get_player_info,
    get_skater_leaders,
    get_skater_stats,
)
from schemas import (
    GoalieCareerInfo,
    GoalieInfo,
    GoalieLeaderboard,
    GoalieStats,
    PlayerInfo,
    SkaterCareerInfo,
    SkaterLeaderboard,
    SkaterStats,
)

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/skaters", response_model=list[SkaterStats])
async def skater_stats(season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id = await get_current_regular_season_id(conn)
    return await get_skater_stats(conn, season_id)


@router.get("/skaters/leaderboard", response_model=list[SkaterLeaderboard])
async def skater_leaders(
    stat: Literal["goals", "assists", "points"] = "goals",
    season_id: int | None = None,
    conn: AsyncConnection = Depends(get_conn),
):
    if season_id is None:
        season_id = await get_current_regular_season_id(conn)
    return await get_skater_leaders(conn, season_id, stat)


@router.get("/skaters/{player_id}", response_model=PlayerInfo)
async def player_info(
    player_id: int, season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)
):
    if season_id is None:
        season_id = await get_current_regular_season_id(conn)
    result = await get_player_info(conn, season_id, player_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return result


@router.get("/skaters/{player_id}/career", response_model=list[SkaterCareerInfo])
async def player_history(player_id: int, conn: AsyncConnection = Depends(get_conn)):
    history = await get_player_career(conn, player_id)
    if not history:
        raise HTTPException(status_code=404, detail="Player history not found")
    return history


@router.get("/goalies", response_model=list[GoalieStats])
async def goalie_stats(season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id = await get_current_regular_season_id(conn)
    return await get_goalie_stats(conn, season_id)


@router.get("/goalies/leaderboard", response_model=list[GoalieLeaderboard])
async def goalie_leaders(
    stat: Literal["wins", "save_percentage", "shutouts"] = "wins",
    season_id: int | None = None,
    conn: AsyncConnection = Depends(get_conn),
):
    if season_id is None:
        season_id = await get_current_regular_season_id(conn)
    return await get_goalie_leaders(conn, season_id, stat)


@router.get("/goalies/{player_id}", response_model=GoalieInfo)
async def goalie_info(
    player_id: int, season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)
):
    if season_id is None:
        season_id = await get_current_regular_season_id(conn)
    result = await get_goalie_info(conn, season_id, player_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Goalie not found")
    return result


@router.get("/goalies/{player_id}/career", response_model=list[GoalieCareerInfo])
async def goalie_history(player_id: int, conn: AsyncConnection = Depends(get_conn)):
    history = await get_goalie_career(conn, player_id)
    if not history:
        raise HTTPException(status_code=404, detail="Goalie history not found")
    return history
