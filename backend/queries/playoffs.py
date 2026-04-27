from psycopg import AsyncConnection
from psycopg.rows import dict_row


async def get_bracket(conn: AsyncConnection, season_id: int) -> list[dict]:
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """
            SELECT
                pr.round_number,
                pr.round_name,
                ps.series_letter,
                ps.series_name,
                ps.team1_wins,
                ps.team2_wins,
                ps.is_active,
                t1.name  AS team1_name,
                t1.logo_url  AS team1_logo_url,
                t1.code  AS team1_code,
                t2.name  AS team2_name,
                t2.logo_url AS team2_logo_url,
                t2.code  AS team2_code
            FROM playoff_rounds pr
            JOIN playoff_series ps ON ps.round_id = pr.id
            JOIN teams t1 ON t1.id = ps.team1_id
            JOIN teams t2 ON t2.id = ps.team2_id
            WHERE pr.season_id = %s
            ORDER BY pr.round_number, ps.series_letter
            """,
            (season_id,),
        )
        rows = await cur.fetchall()

    # Group flat rows into round -> series structure
    rounds: dict[int, dict] = {}
    for row in rows:
        rnum = row["round_number"]
        if rnum not in rounds:
            rounds[rnum] = {
                "round_number": rnum,
                "round_name": row["round_name"],
                "series": [],
            }
        rounds[rnum]["series"].append(
            {
                "series_letter": row["series_letter"],
                "series_name": row["series_name"],
                "team1": {
                    "name": row["team1_name"],
                    "code": row["team1_code"],
                    "logo_url": row["team1_logo_url"],
                },
                "team2": {
                    "name": row["team2_name"],
                    "code": row["team2_code"],
                    "logo_url": row["team2_logo_url"],
                },
                "team1_wins": row["team1_wins"],
                "team2_wins": row["team2_wins"],
                "is_active": row["is_active"],
            }
        )

    return list(rounds.values())
