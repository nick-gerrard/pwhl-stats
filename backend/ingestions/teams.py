import asyncio

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
            seasons.sort(key=lambda s: s["season_id"], reverse=True)

            teams: dict[str, dict] = {}
            for season in seasons:
                teams_url = f"https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=teamsbyseason&season_id={season['season_id']}&key=446521baf8c38984&client_code=pwhl"
                response = await client.get(teams_url)
                response.raise_for_status()
                for team in response.json()["SiteKit"]["Teamsbyseason"]:
                    teams.setdefault(team["id"], {
                        "api_id": team["id"],
                        "name": team["name"],
                        "city": team["city"],
                        "code": team["code"],
                        "nickname": team["nickname"],
                        "logo_url": team["team_logo_url"],
                    })

        for team in teams.values():
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
                    team["api_id"],
                    team["name"],
                    team["city"],
                    team["code"],
                    team["nickname"],
                    team["logo_url"],
                ),
            )

        await conn.commit()


if __name__ == "__main__":
    asyncio.run(run())
