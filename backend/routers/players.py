from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn
from queries.players import get_players

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/")
async def players(conn: AsyncConnection = Depends(get_conn)):
    return await get_players(conn)
