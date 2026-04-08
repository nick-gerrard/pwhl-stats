"""Shared database utilities for ingestion scripts."""

from contextlib import asynccontextmanager
from datetime import date

import psycopg

from settings import settings


@asynccontextmanager
async def get_connection():
    """Async context manager providing a psycopg connection."""
    async with await psycopg.AsyncConnection.connect(settings.database_url) as conn:
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


async def get_all_seasons(conn) -> list[tuple[int, int, str]]:
    """
    Returns list of (internal_id, api_id, season_type) for all non-preseason seasons.
    Use season_type to filter: 'regular', 'playoff', or 'preseason'.
    """
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT id, api_id, season_type FROM seasons WHERE season_type != 'preseason' ORDER BY api_id"
        )
        return await cur.fetchall()


async def get_team_id_map(conn) -> dict[str, int]:
    """
    Returns a mapping of api_id -> internal id for all teams.
    Used to resolve HockeyTech team IDs to our own IDs.
    """
    async with conn.cursor() as cur:
        await cur.execute("SELECT api_id, id FROM teams")
        rows = await cur.fetchall()
        return {str(row[0]): row[1] for row in rows}
