from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn
from queries.teams import get_teams
from schemas import Team

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[Team])
async def teams(conn: AsyncConnection = Depends(get_conn)):
    return await get_teams(conn)
