import asyncio

from psycopg import AsyncConnection
from psycopg.rows import dict_row

from ingestions.run import run_all
from live.firebase import fetch_live_games

live_state: dict = {}
clients: set = set()


def _all_games_final(live_state: dict, expected_ids: set[str]) -> bool:
    return all(
        live_state.get(gid, {}).get("status") == "Final"
        for gid in expected_ids
    )


async def check_start_time(conn: AsyncConnection):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT MIN(start_time) AS start_time
               FROM games
               WHERE start_time::date = CURRENT_DATE
               """,
        )
        return await cur.fetchone()


async def get_today_game_ids(conn: AsyncConnection) -> set[str]:
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT api_id FROM games WHERE date = CURRENT_DATE"
        )
        rows = await cur.fetchall()
        return {str(row[0]) for row in rows}


async def populate_live_state():
    live_state.update(await fetch_live_games())


async def polling_loop(expected_ids: set[str]):
    while not _all_games_final(live_state, expected_ids):
        await populate_live_state()

        for queue in clients:
            await queue.put(live_state)

        if not _all_games_final(live_state, expected_ids):
            await asyncio.sleep(10)

    await asyncio.sleep(20 * 60)
    await run_all()
