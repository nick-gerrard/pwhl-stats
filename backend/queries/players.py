from psycopg import AsyncConnection
from psycopg.rows import dict_row


async def get_players(conn: AsyncConnection):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT id, api_id, first_name, last_name, shoots, position 
            FROM players
            WHERE active = TRUE 
            ORDER BY last_name"""
        )
        return await cur.fetchall()
