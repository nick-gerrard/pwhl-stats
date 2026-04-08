from fastapi import APIRouter, Depends
from psycopg import AsyncConnection

from database import get_conn
from queries.seasons import get_seasons
from schemas import Season

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.get("/", response_model=list[Season])
async def seasons(conn: AsyncConnection = Depends(get_conn)):
    return await get_seasons(conn)
