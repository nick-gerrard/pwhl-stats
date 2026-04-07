from psycopg import AsyncConnection
from psycopg.rows import dict_row


async def get_standings(conn: AsyncConnection, season_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT t.name AS team_name, s.games_played,
            wins, losses, ot_wins, ot_losses, shootout_wins, 
            shootout_losses, points
               FROM standings s
               JOIN teams t ON t.id = s.team_id
               WHERE s.season_id = %s
               ORDER BY s.points DESC""",
            (season_id,),
        )
        return await cur.fetchall()
