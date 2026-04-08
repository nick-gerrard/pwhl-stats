from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn, get_current_season
from queries.standings import get_standings
from schemas import Standing

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get("/", response_model=list[Standing])
async def standings(season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id, _ = await get_current_season(conn)
    return await get_standings(conn, season_id)
