from psycopg import AsyncConnection
from psycopg.rows import dict_row


async def get_teams(conn: AsyncConnection):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT id, api_id, name, city, code, nickname, logo_url 
            FROM teams 
            ORDER BY name"""
        )
        return await cur.fetchall()
