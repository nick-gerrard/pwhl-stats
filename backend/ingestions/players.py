"""Ingest player profiles from team rosters across all regular seasons."""

import asyncio
from datetime import date

import httpx

from ingestions.db import get_all_seasons, get_connection, get_team_id_map

BASE_URL = "https://lscluster.hockeytech.com/feed/index.php"
AUTH = "key=446521baf8c38984&client_code=pwhl"


def parse_height(height: str):
    if not height:
        return None
    try:
        feet, inches = height.replace('"', "").split("'")
        return int(feet) * 12 + int(inches)
    except (ValueError, AttributeError):
        return None


async def run():
    async with get_connection() as conn:
        seasons = await get_all_seasons(conn)
        team_id_map = await get_team_id_map(conn)

        async with httpx.AsyncClient() as client:
            for _season_id, season_api_id, season_type in seasons:
                if season_type != "regular":
                    continue

                for team_api_id in team_id_map:
                    url = f"{BASE_URL}?feed=modulekit&view=roster&team_id={team_api_id}&season_id={season_api_id}&{AUTH}"
                    response = await client.get(url)
                    response.raise_for_status()

                    players = response.json()["SiteKit"]["Roster"]

                    for player in players:
                        if not isinstance(player, dict):
                            continue

                        await conn.execute(
                            """
                            INSERT INTO players (api_id, first_name, last_name, height, weight,
                                                 birthdate, nationality, shoots, position, active)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (api_id) DO UPDATE SET
                                first_name = EXCLUDED.first_name,
                                last_name = EXCLUDED.last_name,
                                height = EXCLUDED.height,
                                weight = EXCLUDED.weight,
                                birthdate = EXCLUDED.birthdate,
                                nationality = EXCLUDED.nationality,
                                shoots = EXCLUDED.shoots,
                                position = EXCLUDED.position,
                                active = EXCLUDED.active
                            """,
                            (
                                player["id"],
                                player["first_name"],
                                player["last_name"],
                                parse_height(player["height"]),
                                int(player["weight"]) if player["weight"] else None,
                                date.fromisoformat(player["birthdate"]) if player["birthdate"] else None,
                                player["birthcntry"],
                                player["shoots"],
                                player["position"],
                                bool(player["active"]),
                            ),
                        )

        await conn.commit()
        print("Players ingestion complete.")


if __name__ == "__main__":
    asyncio.run(run())
