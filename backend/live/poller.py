import asyncio

from psycopg import AsyncConnection
from psycopg.rows import dict_row

from ingestions.run import run_all
from live.firebase import fetch_live_games

live_state: dict = {}
clients: set = set()


def _check_game_status(live_state):
    for game in live_state.values():
        if game["status"] != "Final":
            return False
    return True


async def check_start_time(conn: AsyncConnection):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """SELECT MIN(start_time) AS start_time
               FROM games
               WHERE start_time::date = CURRENT_DATE
               """,
        )
        return await cur.fetchone()


async def populate_live_state():
    live_state.update(await fetch_live_games())


async def polling_loop():
    all_games_completed = False
    while not all_games_completed:
        await populate_live_state()

        for queue in clients:
            await queue.put(live_state)

        all_games_completed = _check_game_status(live_state)

        if not all_games_completed:
            await asyncio.sleep(10)

    await asyncio.sleep(20 * 60)
    await run_all()
