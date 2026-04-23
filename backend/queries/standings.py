from psycopg import AsyncConnection
from psycopg.rows import dict_row


async def get_standings(conn: AsyncConnection, season_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT t.id AS team_id, t.name AS team_name, t.logo_url AS logo_url,
            s.games_played, regulation_wins, wins, losses, ot_wins, ot_losses,
            shootout_wins, shootout_losses, points
               FROM standings s
               JOIN teams t ON t.id = s.team_id
               WHERE s.season_id = %s
               ORDER BY s.points DESC""",
            (season_id,),
        )
        return await cur.fetchall()
