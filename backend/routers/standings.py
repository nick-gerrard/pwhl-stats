from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn, get_current_regular_season_id
from queries.games import get_remaining_games
from queries.standings import get_standings
from schemas import Standing
from utils import compute_eliminations

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get("/", response_model=list[Standing])
async def standings(season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id = await get_current_regular_season_id(conn)
    rows = await get_standings(conn, season_id)
    remaining = await get_remaining_games(conn, season_id)
    remaining_by_team = {r["id"]: r["remaining_games"] for r in remaining}
    return compute_eliminations(rows, remaining_by_team)
