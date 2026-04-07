from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn, get_current_season
from queries.standings import get_standings

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get("/")
async def standings(conn: AsyncConnection = Depends(get_conn)):
    season_id, _ = await get_current_season(conn)
    return await get_standings(conn, season_id)
