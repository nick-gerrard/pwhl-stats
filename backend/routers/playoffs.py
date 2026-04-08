from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection

from database import get_conn, get_latest_playoff_season
from queries.playoffs import get_bracket
from schemas import PlayoffRound

router = APIRouter(prefix="/playoffs", tags=["playoffs"])


@router.get("/bracket", response_model=list[PlayoffRound])
async def bracket(season_id: int | None = None, conn: AsyncConnection = Depends(get_conn)):
    if season_id is None:
        season_id = await get_latest_playoff_season(conn)
    if season_id is None:
        raise HTTPException(status_code=404, detail="No playoff data found")
    return await get_bracket(conn, season_id)
