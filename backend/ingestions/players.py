import asyncio
from datetime import date

import httpx
import psycopg

from settings import settings


def parse_height(height: str):
    if not height:
        return None

    try:
        feet, inches = height.replace('"', "").split("'")
        return int(feet) * 12 + int(inches)
    except (ValueError, AttributeError):
        return None


async def run():
    async with await psycopg.AsyncConnection.connect(settings.database_url) as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, api_id FROM teams")
            teams = await cur.fetchall()

            await cur.execute(
                "SELECT api_id FROM seasons WHERE start_date <= %s AND end_date >= %s",
                (date.today(), date.today()),
            )
            season = await cur.fetchone()
            if season is None:
                raise RuntimeError("No Active season found in database")
            current_season_api_id = season[0]

            urls = []
            for team in teams:
                roster_url = f"https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=roster&team_id={team[1]}&season_id={current_season_api_id}&key=446521baf8c38984&client_code=pwhl"
                urls.append(roster_url)

            for url in urls:
                async with httpx.AsyncClient() as client:
                    roster_response = await client.get(url)
                    roster_response.raise_for_status()

                    players = roster_response.json()["SiteKit"]["Roster"]
                    print(
                        f"Fetching roster from {url}, got {len(players)} entries, first type: {type(players[0]) if players else 'empty'}"
                    )

                    for player in players:
                        if not isinstance(player, dict):
                            print("SKIPPING...")
                            continue
                        await conn.execute(
                            """
                            INSERT INTO players (api_id, first_name, last_name, height, weight, 
                                                    birthdate, nationality, shoots, position, 
                                                    active)
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
                                date.fromisoformat(player["birthdate"])
                                if player["birthdate"]
                                else None,
                                player["birthcntry"],
                                player["shoots"],
                                player["position"],
                                bool(player["active"]),
                            ),
                        )
            await conn.commit()


if __name__ == "__main__":
    asyncio.run(run())
