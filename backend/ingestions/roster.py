"""Ingest roster data — links players to teams and seasons."""

import asyncio

import httpx

from ingestions.db import get_all_seasons, get_connection, get_team_id_map

BASE_URL = "https://lscluster.hockeytech.com/feed/index.php"
AUTH = "key=446521baf8c38984&client_code=pwhl"


async def run():
    async with get_connection() as conn:
        seasons = await get_all_seasons(conn)
        team_id_map = await get_team_id_map(conn)

        async with conn.cursor() as cur:
            await cur.execute("SELECT api_id, id FROM players")
            rows = await cur.fetchall()
            player_id_map = {str(row[0]): row[1] for row in rows}

        async with httpx.AsyncClient() as client:
            for season_id, season_api_id, season_type in seasons:
                if season_type != "regular":
                    continue

                for team_api_id, team_id in team_id_map.items():
                    url = f"{BASE_URL}?feed=modulekit&view=roster&team_id={team_api_id}&season_id={season_api_id}&{AUTH}"
                    response = await client.get(url)
                    response.raise_for_status()

                    players = response.json()["SiteKit"]["Roster"]

                    for player in players:
                        if not isinstance(player, dict):
                            continue

                        player_internal_id = player_id_map.get(player["person_id"])
                        if player_internal_id is None:
                            continue  # player not in our DB yet, skip

                        jersey = player.get("tp_jersey_number")
                        is_rookie = player.get("rookie", "0") == "1"

                        await conn.execute(
                            """
                            INSERT INTO roster (player_id, team_id, season_id, player_number, is_rookie)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (player_id, team_id, season_id) DO UPDATE SET
                                player_number = EXCLUDED.player_number,
                                is_rookie = EXCLUDED.is_rookie
                            """,
                            (
                                player_internal_id,
                                team_id,
                                season_id,
                                int(jersey) if jersey else None,
                                is_rookie,
                            ),
                        )

        await conn.commit()
        print("Roster ingestion complete.")


if __name__ == "__main__":
    asyncio.run(run())
