import asyncio
from datetime import date

import httpx
import psycopg

from settings import settings


async def run():
    async with await psycopg.AsyncConnection.connect(settings.database_url) as conn:
        seasons_url = "https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=seasons&key=446521baf8c38984&client_code=pwhl"

        async with httpx.AsyncClient() as client:
            season_response = await client.get(seasons_url)
            season_response.raise_for_status()

        seasons = season_response.json()["SiteKit"]["Seasons"]
        # Fallback to 5 for season id if the date check fails
        current_season_id = 5
        for season in seasons:
            if (
                date.fromisoformat(season["start_date"])
                <= date.today()
                <= date.fromisoformat(season["end_date"])
            ):
                current_season_id = season["season_id"]

        teams_url = f"https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=teamsbyseason&season_id={current_season_id}&key=446521baf8c38984&client_code=pwhl"

        async with httpx.AsyncClient() as client:
            response = await client.get(teams_url)
            response.raise_for_status()

        response = response.json()

        for team in response["SiteKit"]["Teamsbyseason"]:
            await conn.execute(
                """
                INSERT INTO teams (api_id, name, city, code, nickname, logo_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (api_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    city = EXCLUDED.city,
                    code = EXCLUDED.code,
                    nickname = EXCLUDED.nickname,
                    logo_url = EXCLUDED.logo_url
            """,
                (
                    team["id"],
                    team["name"],
                    team["city"],
                    team["code"],
                    team["nickname"],
                    team["team_logo_url"],
                ),
            )

        await conn.commit()


if __name__ == "__main__":
    asyncio.run(run())
