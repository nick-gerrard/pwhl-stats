from psycopg import AsyncConnection
from psycopg.rows import dict_row


async def get_seasons(conn: AsyncConnection) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """
            SELECT id, name, season_type
            FROM seasons
            WHERE season_type != 'preseason'
            ORDER BY id DESC
            """
        )
        return await cur.fetchall()
