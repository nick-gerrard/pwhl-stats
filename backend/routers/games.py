from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn, get_current_season
from queries.games import get_games
from schemas import Game

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=list[Game])
async def games(season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id, _ = await get_current_season(conn)
    return await get_games(conn, season_id)
