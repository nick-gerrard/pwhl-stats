# queries/stats.py
from psycopg import AsyncConnection
from psycopg.rows import dict_row


async def get_skater_stats(conn: AsyncConnection, season_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT p.first_name, p.last_name, t.name AS team_name,
                      ss.goals, ss.assists, ss.shots
               FROM skater_stats ss
               JOIN players p ON p.id = ss.player_id
               JOIN teams t ON t.id = ss.team_id
               WHERE ss.season_id = %s
               ORDER BY ss.goals DESC""",
            (season_id,),
        )
        return await cur.fetchall()


async def get_goalie_stats(conn: AsyncConnection, season_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT p.first_name, p.last_name, t.name AS team_name, wins, shutouts, save_percentage 
            FROM goalie_stats gs
            JOIN players p on p.id = gs.player_id
            JOIN teams t on t.id = gs.team_id
            WHERE gs.season_id = %s
            ORDER BY save_percentage DESC""",
            (season_id,),
        )
        return await cur.fetchall()
