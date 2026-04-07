from psycopg import AsyncConnection
from psycopg.rows import dict_row


async def get_games(conn: AsyncConnection, season_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT home_team.name AS home_team, visiting_team.name AS visiting_team, home_score, away_score, date, status
               FROM games g
               JOIN teams home_team ON home_team.id = g.home_team_id
               JOIN teams visiting_team ON visiting_team.id = g.visiting_team_id
               WHERE g.season_id = %s
               ORDER BY date""",
            (season_id,),
        )
        return await cur.fetchall()
