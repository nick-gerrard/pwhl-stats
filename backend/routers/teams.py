from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn
from queries.teams import get_teams

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/")
async def teams(conn: AsyncConnection = Depends(get_conn)):
    return await get_teams(conn)
