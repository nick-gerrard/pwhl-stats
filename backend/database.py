from datetime import date

from psycopg_pool import AsyncConnectionPool

pool: AsyncConnectionPool | None = None


async def get_conn():
    assert pool is not None, "Database pool is not initialized"
    async with pool.connection() as conn:
        yield conn


async def get_current_season(conn) -> tuple[int, int]:
    """
    Returns (internal_id, api_id) of the current active season.
    Raises RuntimeError if no active season is found.
    """
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT id, api_id FROM seasons WHERE start_date <= %s AND end_date >= %s",
            (date.today(), date.today()),
        )
        season = await cur.fetchone()
        if season is None:
            raise RuntimeError("No active season found in database")
        return season[0], season[1]


async def get_current_playoff_season_id(conn) -> int | None:
    """
    Returns the internal id of the most recent playoff season, but only if it belongs
    to the current regular-season cycle. Returns None if playoffs haven't started yet
    for this season (i.e. the most recent playoff ended before the current regular
    season started).
    """
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT id, end_date FROM seasons WHERE season_type = 'playoff' ORDER BY end_date DESC LIMIT 1"
        )
        playoff = await cur.fetchone()
        if playoff is None:
            return None
        playoff_id, playoff_end = playoff

        await cur.execute(
            "SELECT start_date FROM seasons WHERE season_type = 'regular' ORDER BY start_date DESC LIMIT 1"
        )
        regular = await cur.fetchone()
        if regular is None:
            return playoff_id

        # Playoff ended before the current regular season started → belongs to last cycle
        if playoff_end < regular[0]:
            return None
        return playoff_id


async def get_team_id_map(conn) -> dict[str, int]:
    """
    Returns a mapping of api_id -> internal id for all teams.
    Used to resolve HockeyTech team IDs to our own IDs.
    """
    async with conn.cursor() as cur:
        await cur.execute("SELECT api_id, id FROM teams")
        rows = await cur.fetchall()
        return {str(row[0]): row[1] for row in rows}
