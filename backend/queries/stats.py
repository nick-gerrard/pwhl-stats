# queries/stats.py
from psycopg import AsyncConnection, sql
from psycopg.rows import dict_row


async def get_skater_stats(conn: AsyncConnection, season_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT p.id AS player_id, p.first_name, p.last_name, t.name AS team_name,
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
            """SELECT p.id AS player_id, p.first_name, p.last_name, t.name AS team_name,
                      gs.wins, gs.shutouts, gs.save_percentage
            FROM goalie_stats gs
            JOIN players p on p.id = gs.player_id
            JOIN teams t on t.id = gs.team_id
            WHERE gs.season_id = %s
            ORDER BY save_percentage DESC""",
            (season_id,),
        )
        return await cur.fetchall()


async def get_player_info(conn: AsyncConnection, season_id: int, player_id: int) -> dict | None:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT p.first_name, p.last_name, t.name as team_name,
                ss.games_played, ss.goals, ss.assists, ss.pim, ss.plus_minus,
                ss.shots, ss.avg_toi, ss.pp_goals, ss.sh_goals, ss.gw_goals,
                p.height, p.weight, p.birthdate, p.nationality, p.shoots, p.position,
                p.active
                FROM skater_stats ss
                JOIN players p ON p.id = ss.player_id
                JOIN teams t ON t.id = ss.team_id
                WHERE ss.season_id = %s AND ss.player_id = %s
            """,
            (season_id, player_id),
        )
        return await cur.fetchone()


async def get_goalie_info(conn: AsyncConnection, season_id: int, player_id: int) -> dict | None:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT p.first_name, p.last_name, t.name as team_name,
                gs.games_played, gs.wins, gs.losses, gs.ot_losses, gs.shutouts,
                gs.shots_against, gs.goals_against, gs.save_percentage, gs.gaa,
                gs.minutes_played,
                p.height, p.weight, p.birthdate, p.nationality, p.shoots, p.position,
                p.active
                FROM goalie_stats gs
                JOIN players p ON p.id = gs.player_id
                JOIN teams t ON t.id = gs.team_id
                WHERE gs.season_id = %s AND gs.player_id = %s
            """,
            (season_id, player_id),
        )
        return await cur.fetchone()


async def get_player_career(conn: AsyncConnection, player_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT p.first_name, p.last_name, t.name as team_name,
                ss.games_played, ss.goals, ss.assists, ss.pim, ss.plus_minus,
                ss.shots, ss.avg_toi, ss.pp_goals, ss.sh_goals, ss.gw_goals,
                p.height, p.weight, p.birthdate, p.nationality, p.shoots, p.position,
                p.active, ss.season_id, s.start_date, s.end_date, p.api_id
                FROM skater_stats ss
                JOIN players p ON p.id = ss.player_id
                JOIN teams t ON t.id = ss.team_id
                JOIN seasons s on s.id = ss.season_id
                WHERE s.season_type = 'regular' AND ss.player_id = %s
                ORDER BY s.start_date ASC
            """,
            (player_id,),
        )
        return await cur.fetchall()


async def get_goalie_career(conn: AsyncConnection, player_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """
            SELECT p.first_name, p.last_name, t.name as team_name,
                gs.games_played, gs.wins, gs.losses, gs.ot_losses, gs.shutouts,
                gs.shots_against, gs.goals_against, gs.save_percentage, gs.gaa,
                gs.minutes_played, p.height, p.weight, p.birthdate, p.nationality, p.shoots,
                p.position, p.active, gs.season_id, s.start_date, s.end_date, p.api_id
                FROM goalie_stats gs
                JOIN players p on p.id = gs.player_id
                JOIN teams t on t.id = gs.team_id
                JOIN seasons s on s.id = gs.season_id
                WHERE s.season_type = 'regular' AND gs.player_id = %s
                ORDER BY s.start_date ASC
            """,
            (player_id,),
        )
        return await cur.fetchall()


async def get_skater_leaders(conn: AsyncConnection, season_id: int, stat="goals") -> list[dict]:
    ALLOWED_STATS = {"goals", "assists", "points"}
    async with conn.cursor(row_factory=dict_row) as cur:
        if stat not in ALLOWED_STATS:
            raise ValueError(f"Invalid stat: {stat}")

        await cur.execute(
            sql.SQL("""
            SELECT p.first_name, p.last_name, t.name as team_name,
            ss.goals, ss.assists, ss.goals + ss.assists AS points
            FROM skater_stats ss
            JOIN players p on p.id = ss.player_id
            JOIN teams t on t.id = ss.team_id
            WHERE ss.season_id = %s
            ORDER BY {stat} DESC
            LIMIT 10
            """).format(stat=sql.Identifier(stat)),
            (season_id,),
        )
        return await cur.fetchall()


async def get_goalie_leaders(conn: AsyncConnection, season_id: int, stat="wins") -> list[dict]:
    ALLOWED_STATS = {"save_percentage", "wins", "shutouts"}
    async with conn.cursor(row_factory=dict_row) as cur:
        if stat not in ALLOWED_STATS:
            raise ValueError(f"Invalid stat: {stat}")

        await cur.execute(
            sql.SQL("""
            SELECT p.first_name, p.last_name, t.name as team_name,
            gs.wins, gs.save_percentage, gs.shutouts, gs.gaa
            FROM goalie_stats gs
            JOIN players p on p.id = gs.player_id
            JOIN teams t on t.id = gs.team_id
            WHERE gs.season_id = %s
            ORDER BY {stat} DESC
            LIMIT 10
            """).format(stat=sql.Identifier(stat)),
            (season_id,),
        )
        return await cur.fetchall()
