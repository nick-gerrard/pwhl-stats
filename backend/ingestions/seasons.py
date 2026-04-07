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

        for season in seasons:
            await conn.execute(
                """
                INSERT INTO seasons (api_id, name, start_date, end_date)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (api_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date
            """,
                (
                    season["season_id"],
                    season["season_name"],
                    date.fromisoformat(season["start_date"]),
                    date.fromisoformat(season["end_date"]),
                ),
            )
        await conn.commit()


if __name__ == "__main__":
    asyncio.run(run())
